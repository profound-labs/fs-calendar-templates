package main

import (
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"

	"github.com/splendidmoons/suriya-go"
)

// File paths are relative to project root, because "go run ..." is called by
// the Makefile from there.

func main() {
	args := os.Args[1:]
	if len(args) == 0 {
		fmt.Println("First argument must be the year.")
		os.Exit(2)
	}

	calendarYear, err := strconv.Atoi(args[0])
	if err != nil {
		fmt.Printf("Can't parse as year: %s\n", args[0])
		os.Exit(2)
	}
	if calendarYear < 2000 || calendarYear > 2100 {
		fmt.Println("Expected a year between 2000 - 2100.")
		os.Exit(2)
	}

	var events EventSlice

	events = append(events, getAnnuals(calendarYear)...)
	events = append(events, getMoondays(calendarYear)...)

	events.WriteToCsv("./data/events.csv")

	events = getAstroMoondays(calendarYear)
	events.WriteToCsv("./data/astromoondays.csv")
}

type Event struct {
	Date         time.Time
	DayText      string
	Note         string
	Label        string
	Phase        string
	Season       string
	SeasonNumber int
	SeasonTotal  int
	Days         int
}

func (e Event) CsvString(sep string) string {
	fields := []string{
		e.Date.Format("2006-01-02"),
		e.DayText,
		e.Note,
		e.Label,
		e.Phase,
		e.Season,
		fmt.Sprintf("%d", e.SeasonNumber),
		fmt.Sprintf("%d", e.SeasonTotal),
		fmt.Sprintf("%d", e.Days),
	}

	return fmt.Sprintf("%s\n", strings.Join(fields, sep))
}

type EventSlice []Event

func (s EventSlice) Len() int {
	return len(s)
}

func (s EventSlice) Less(i, j int) bool {
	return s[i].Date.Before(s[j].Date)
}

func (s EventSlice) Swap(i, j int) {
	s[i], s[j] = s[j], s[i]
}

func (rows EventSlice) WriteToCsv(path string) {
	f, err := os.Create(path)
	check(err)
	defer f.Close()

	sort.Sort(rows)

	_, err = f.WriteString(fmt.Sprintf("date;day_text;note;label;phase;season;season_number;season_total;days\n"))
	check(err)

	for _, row := range rows {
		_, err = f.WriteString(row.CsvString(";"))
		check(err)
	}
}

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func getMoondays(calendarYear int) EventSlice {
	fromDate, _ := time.Parse("2006-01-02", fmt.Sprintf("%d-01-01", calendarYear))
	toDate, _ := time.Parse("2006-01-02", fmt.Sprintf("%d-12-31", calendarYear))

	var events EventSlice

	days := suriya.GetCalDays(fromDate, toDate)
	for _, d := range days {

		// they all have to be strings
		phase, label, season := "", "", ""
		season_number, season_total, days := 0, 0, 0
		if len(d.UposathaMoon) > 0 {
			u := d.UposathaMoon[0]
			phase = u.Phase
			label = u.Event
			season_number = u.S_Number
			season_total = u.S_Total
			days = u.U_Days

			switch u.LunarSeason {
			case 1:
				season = "Hemanta"
			case 2:
				season = "Gimha"
			case 3:
				season = "Vassāna"
			}
		} else if len(d.HalfMoon) > 0 {
			phase = d.HalfMoon[0].Phase
		} else {
			continue
		}

		day_text := ""
		switch phase {
		case "new":
			day_text = "\\NewMoon"
		case "waxing":
			day_text = "\\FirstQuarter"
		case "full":
			day_text = "\\FullMoon"
		case "waning":
			day_text = "\\LastQuarter"
		}

		e := Event{
			Date:         d.Date,
			DayText:      day_text,
			Note:         "",
			Label:        label,
			Phase:        phase,
			Season:       season,
			SeasonNumber: season_number,
			SeasonTotal:  season_total,
			Days:         days,
		}

		events = append(events, e)
	}

	return events
}

func getAstroMoondays(calendarYear int) EventSlice {
	fromDate, _ := time.Parse("2006-01-02", fmt.Sprintf("%d-01-01", calendarYear))
	toDate, _ := time.Parse("2006-01-02", fmt.Sprintf("%d-12-31", calendarYear))

	var events EventSlice

	days := suriya.GetCalDays(fromDate, toDate)
	for _, d := range days {

		phase := ""
		if len(d.AstroMoon) > 0 {
			m := d.GetAstroMoon()
			phase = m.Phase
		} else {
			continue
		}

		e := Event{
			Date:         d.Date,
			DayText:      "",
			Note:         "",
			Label:        "",
			Phase:        phase,
			Season:       "",
			SeasonNumber: 0,
			SeasonTotal:  0,
			Days:         0,
		}

		events = append(events, e)
	}

	return events
}

func getAnnuals(calendarYear int) EventSlice {
	events := GenerateSolarYearEvents(calendarYear)

	// January 16: Ajahn Chah Memorial Day
	date, _ := time.Parse("2006-01-02", fmt.Sprintf("%d-01-16", calendarYear))
	e := Event{
		Date:  date,
		Note:  "\\xAjahnChahMemorialDay",
		Label: "aj-chah-memorial",
	}
	events = append(events, e)

	// June 17: Ajahn Chah's Birthday
	date, _ = time.Parse("2006-01-02", fmt.Sprintf("%d-06-17", calendarYear))
	e = Event{
		Date:  date,
		Note:  "\\xAjahnChahBirthDay",
		Label: "aj-chah-birthday",
	}
	events = append(events, e)

	// April 13: Thai New Year, Songkran
	date, _ = time.Parse("2006-01-02", fmt.Sprintf("%d-04-13", calendarYear))
	e = Event{
		Date:  date,
		Note:  "\\xThaiNewYear",
		Label: "thai-new-year",
	}
	events = append(events, e)

	return events
}

// A variation on suriya.GenerateSolarYear(). Collecting only the major moondays
// and associated events, using LaTeX translation placeholder commands as note
// text.

func GenerateSolarYearEvents(solar_year int) EventSlice {
	var events EventSlice

	var su_year suriya.SuriyaYear
	su_year.Init(solar_year)

	date := suriya.CalculatePreviousKattika(solar_year)

	last_uposatha := suriya.UposathaMoon{
		Date:        date,
		Calendar:    0, // mahanikaya
		Phase:       "full",
		S_Number:    8,
		S_Total:     8,
		U_Days:      15,
		M_Days:      29,
		LunarMonth:  12,
		LunarSeason: 3,
		LunarYear:   date.Year() + suriya.BEdiff,
	}

	for last_uposatha.Date.Year() <= solar_year {
		var uposatha suriya.UposathaMoon
		uposatha = last_uposatha.NextUposatha()
		last_uposatha = uposatha

		// Major Events

		if uposatha.Date.Year() == solar_year {

			var e Event

			// Magha Puja
			if uposatha.Event == "magha" {
				e = Event{
					Date:    uposatha.Date,
					Note:    "\\xMaghaPuja", // Māgha Pūjā
					Label:   "magha",
					DayText: "\\FullMoon",
				}
				events = append(events, e)
			}

			// Vesakha Puja
			if uposatha.Event == "vesakha" {
				e = Event{
					Date:    uposatha.Date,
					Note:    "\\xVesakhaPuja", // Vesākha Pūjā
					Label:   "vesakha",
					DayText: "\\FullMoon",
				}
				events = append(events, e)
			}

			// Asalha Puja
			// First Day of Vassa
			if uposatha.Event == "asalha" {
				e = Event{
					Date:    uposatha.Date,
					Note:    "\\xAsalhaPuja", // Āsāḷha Pūjā
					Label:   "asalha",
					DayText: "\\FullMoon",
				}
				events = append(events, e)

				e = Event{
					Date:  uposatha.Date.AddDate(0, 0, 1),
					Note:  "\\xFirstDayOfVassa",
					Label: "first-day",
				}
				events = append(events, e)
			}

			// Pavarana
			// Last Day of Vassa
			if uposatha.Event == "pavarana" {
				e = Event{
					Date:    uposatha.Date,
					Note:    "\\xPavarana",
					Label:   "pavarana",
					DayText: "\\FullMoon",
				}
				events = append(events, e)

				e = Event{
					Date:    uposatha.Date,
					Note:    "\\xLastDayOfVassa",
					Label:   "last-day",
					DayText: "\\FullMoon",
				}
				events = append(events, e)
			}
		}
	}

	return events
}
