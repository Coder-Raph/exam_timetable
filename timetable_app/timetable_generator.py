# timetable_generator.py
import random
from datetime import datetime, timedelta
from timetable_app.models import TimetableSlot, Venue, Rule

def generate_timetable():
    # Retrieve venues and rules from the database
    venues = Venue.objects.all()
    rules = Rule.objects.all()

    # Generate timetable slots
    timetable_slots = []
    start_date = datetime.now().date()

    for day in range(5):  # Assuming a week with 5 days (adjust as needed)
        current_date = start_date + timedelta(days=day)

        for venue in venues:
            # Example: Get available rules for the venue
            available_rules = rules.filter(venue=venue)

            # Example: Generate a random duration for the slot (adjust as needed)
            duration_options = [timedelta(hours=1), timedelta(hours=2)]
            duration = random.choice(duration_options)

            # Create a timetable slot
            slot = TimetableSlot.objects.create(
                day=current_date,
                start_time=datetime.now().time(),  # Adjust as needed
                end_time=(datetime.now() + duration).time(),  # Adjust as needed
                duration=duration,
                faculty="Example Faculty",
                course_file=None,  # Adjust as needed
                venue=venue,
            )

            # Example: Assign random rules to the slot (adjust as needed)
            slot.rules.set(random.sample(list(available_rules), random.randint(0, len(available_rules))))

            timetable_slots.append(slot)

    return timetable_slots

if __name__ == "__main__":
    # Run the timetable generation
    generated_timetable = generate_timetable()

    # Print the generated timetable slots
    for slot in generated_timetable:
        print(f"Timetable Slot: {slot}")
