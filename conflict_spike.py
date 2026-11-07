
# Function to check whether two events overlap
def check_conflict(event1, event2):

    # datecheck
    if event1["date"] != event2["date"]:
        return False

    # Get the starting and ending times
    start1 = event1["start"]
    end1 = event1["end"]

    start2 = event2["start"]
    end2 = event2["end"]

    # Check whether the time periods overlap
    if start1 < end2 and start2 < end1:
        return True
    else:
        return False


# Create StudentSync schedule events
class_event = {
    "title": "Calculus Class",
    "date": "2026-11-06",
    "start": 14.0,
    "end": 15.5
}

work_event = {
    "title": "Library Work Shift",
    "date": "2026-11-06",
    "start": 15.0,
    "end": 17.0
}

study_event = {
    "title": "Study Session",
    "date": "2026-11-06",
    "start": 17.0,
    "end": 18.0
}


# Store all events in a list
events = [class_event, work_event, study_event]


# Compare every pair of events
for i in range(len(events)):
    for j in range(i + 1, len(events)):

        event1 = events[i]
        event2 = events[j]

        if check_conflict(event1, event2):
            print("CONFLICT:", event1["title"],
                  "overlaps with", event2["title"])
        else:
            print("NO CONFLICT:", event1["title"],
                  "and", event2["title"])
