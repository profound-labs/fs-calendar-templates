local date = require("wallcalendar-date.lua")
local csv = require("wallcalendar-csv.lua")
local tsp = tex.sprint
require("wallcalendar-helpers.lua")

function isUposatha(event)
  return event.phase == "full" or event.phase == "new"
end

function hasNote(event)
  return ok(event.note)
end

function eventFmtUposathas(idx, max_idx, event, event_date, mark)
  if ok(event.date) then
    local fmtStr = "\\x%sShort\\ %s & %s & %s \\xDays & %s & %s/%s \\\\"
    local d = event_date
    tsp(string.format(fmtStr, d:fmt("%b"), d:getday(), event.day_text, event.days, event.season, event.season_number, event.season_total))
  else
    tsp(" & & & & \\\\")
  end
end

function eventFmtNotes(idx, max_idx, event, event_date, mark)
  if ok(event.date) then
    local fmtStr = "\\textsuperscript{%s} & \\x%sShort\\ %s: & %s \\\\"
    local d = event_date
    tsp(string.format(fmtStr, mark.symbol, d:fmt("%b"), d:getday(), event.note))
  else
    tsp(" & & \\\\")
  end
end

function setDateTexts(yearNum, language, eventsCsv)
  local names = {"Magha", "Vesakha", "Asalha", "Pavarana"}

  for k,v in pairs(names) do
    local pred = function(e) return e.label == string.lower(v) end
    local event = eventsInYear(loadCsv(eventsCsv), yearNum, pred)[1]
    if ok(event) then
      local d = date(event.date)
      if language == "portuguese" then
        tsp(string.format("\\renewcommand\\xDate".. v .."{%s de \\x%s}", d:getday(), d:fmt("%B")))
      else
        tsp(string.format("\\renewcommand\\xDate".. v .."{\\x%s\\ %s}", d:fmt("%B"), d:getday()))
      end
    end
  end

  local pred = function(e) return e.label == "first-day" end
  local event = eventsInYear(loadCsv(eventsCsv), yearNum, pred)[1]
  if ok(event) then
    local d = date(event.date)
    tsp(string.format("\\renewcommand\\xDateFirstDayOfVassaISO{%s-%s-%s}", d:getyear(), d:getmonth(), d:getday()))
  end

  local pred = function(e) return e.label == "last-day" end
  local event = eventsInYear(loadCsv(eventsCsv), yearNum, pred)[1]
  if ok(event) then
    local d = date(event.date)
    tsp(string.format("\\renewcommand\\xDateLastDayOfVassaISO{%s-%s-%s}", d:getyear(), d:getmonth(), d:getday()))
  end
end

function drawAstroMarks(eventsCsv)
  local command = {
    full = "\\FullAstroMoon",
    waning = "\\LastQuarterAstroMoon",
    new = "\\NewAstroMoon",
    waxing = "\\FirstQuarterAstroMoon"
  }

  local events = loadCsv(eventsCsv)
  for idx,event in pairs(events) do
    tsp("\\draw[gold] node [below right=-3mm and -1.3mm of cal-" ..
          event.date ..
          ".south east] {" ..
          command[event.phase] ..
          "}; ")
  end
end

-- Based on monthMarksDayText() in wallcalendar-helpers.lua, using the day text
-- marks (moondays) as corner marks instead of being day texts.
function monthMarksDayTextAsCornerMarks(monthName, filterPred, eventsCsv)
  local monthNum = monthNameToNum(monthName)
  local events = eventsInMonth(loadCsv(eventsCsv), monthNum, filterPred);

  -- The different moon marks need different offsets if the shapes are different
  -- sizes. Here, the line width for the full moon makes it a different size.

  local do_test_alignment = false

  local spacing = {
    full   = "-10.35pt and 7pt",
    waning = "-10.2pt and 7.15pt",
    new    = "-10.2pt and 7.15pt",
    waxing = "-10.2pt and 7.15pt"
  }

  local command = {
    full = "\\FullMoon",
    waning = "\\LastQuarter",
    new = "\\NewMoon",
    waxing = "\\FirstQuarter"
  }

  local opacity = {
    full = 0.5,
    waning = 0,
    new = 0,
    waxing = 0.5
  }

  local phases = {"full", "waning", "new", "waxing"}

  for idx,event in pairs(events) do
    if ok(event.phase) then
      local d = date(event.date)

      if do_test_alignment then
        for k,v in pairs(phases) do
          tsp(string.format(" \\draw node [above right=%s of cal%s-%s.north east, opacity=%s] {%s}; ",
                            spacing[v],
                            d:fmt("%m"),
                            event.date,
                            opacity[v],
                            command[v]))
        end
      else
        tsp(string.format(" \\draw node [above right=%s of cal%s-%s.north east] {%s}; ",
                          spacing[event.phase],
                          d:fmt("%m"),
                          event.date,
                          event.day_text))
      end
    end
  end
end

function formatOne(events, idx)
  local event = events[idx]
  local mark = getMark(idx, events, nil, true)
  local d = date(event.date)

  local date_as_text = "\\x"..d:fmt("%b").."Short\\space "..d:getday()
  local mark_as_text = "\\s{"..mark.symbol.."}"

  return mark_as_text .. " \\textit{" .. date_as_text .. ":} & " .. event.note
end

function formatThreeForTable(events, indexes)
  tsp(formatOne(events, indexes[1]) .. " & " ..
      formatOne(events, indexes[2]) .. " & " ..
      formatOne(events, indexes[3]) .. " \\\\\n")
end

-- NOTE: hard-coded for 9 events
function formatEventsAsThreeColsTable(events)
  if #events < 9 then
    d = 9 - #events
    for i=0,d,1 do
      events[#events + 1] = {}
    end
  end

  tsp("\\begin{tabular}{l @{\\tabgap} l @{\\tabcolgap} l @{\\tabgap} l @{\\tabcolgap} l @{\\tabgap} l}\n")

  formatThreeForTable(events, {1, 4, 7})
  formatThreeForTable(events, {2, 5, 8})
  formatThreeForTable(events, {3, 6, 9})

  tsp("\\end{tabular}\n")
end

function yearEventsAsThreeColsTable(yearNum, filterPred, eventsCsv)
  local events = eventsInYear(loadCsv(eventsCsv), yearNum, filterPred)

  formatEventsAsThreeColsTable(events)
end
