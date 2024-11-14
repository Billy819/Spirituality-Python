import json
from datetime import datetime

class RosaryPrayerTracker:
    def __init__(self, initial_homeless_count=45252):
        self.homeless_count = initial_homeless_count
        self.daily_reduction_rate = 0.05  # 5% reduction per day
        self.history = []
        self.load_progress()
        self.mysteries = {
            "Sunday": "The Glorious Mysteries",
            "Wednesday": "The Glorious Mysteries",
            "Monday": "The Joyful Mysteries",
            "Saturday": "The Joyful Mysteries",
            "Tuesday": "The Sorrowful Mysteries",
            "Friday": "The Sorrowful Mysteries",
            "Thursday": "The Luminous Mysteries"
        }
        self.mystery_guidelines = {
            "The Glorious Mysteries": [
                "The Resurrection of Jesus",
                "The Ascension of Jesus",
                "The Descent of the Holy Spirit",
                "The Assumption of Mary",
                "The Coronation of Mary as Queen of Heaven and Earth"
            ],
            "The Joyful Mysteries": [
                "The Annunciation",
                "The Visitation",
                "The Birth of Jesus",
                "The Presentation of Jesus at the Temple",
                "The Finding of Jesus in the Temple"
            ],
            "The Sorrowful Mysteries": [
                "The Agony in the Garden",
                "The Scourging at the Pillar",
                "The Crowning with Thorns",
                "The Carrying of the Cross",
                "The Crucifixion"
            ],
            "The Luminous Mysteries": [
                "The Baptism of Jesus in the Jordan",
                "The Wedding Feast at Cana",
                "The Proclamation of the Kingdom of God",
                "The Transfiguration",
                "The Institution of the Eucharist"
            ]
        }
        self.bible_readings = {
            "The Glorious Mysteries": [
                "John 11:25 - 'I am the resurrection and the life.'",
                "Luke 24:51 - 'While he was blessing them, he left them and was taken up into heaven.'",
                "Acts 2:3 - 'They saw what seemed to be tongues of fire.'",
                "Revelation 12:1 - 'A woman clothed with the sun, with the moon under her feet.'",
                "Revelation 12:1 - 'On her head a crown of twelve stars.'"
            ],
            "The Joyful Mysteries": [
                "Luke 1:28 - 'Greetings, you who are highly favored! The Lord is with you.'",
                "Luke 1:42 - 'Blessed are you among women, and blessed is the child you will bear.'",
                "Luke 2:7 - 'She wrapped him in cloths and placed him in a manger.'",
                "Luke 2:22 - 'They took him to Jerusalem to present him to the Lord.'",
                "Luke 2:46 - 'After three days they found him in the temple.'"
            ],
            "The Sorrowful Mysteries": [
                "Matthew 26:39 - 'My Father, if it is possible, let this cup pass from me.'",
                "John 19:1 - 'Then Pilate took Jesus and had him flogged.'",
                "Matthew 27:29 - 'They twisted together a crown of thorns and set it on his head.'",
                "John 19:17 - 'Carrying his own cross, he went out to the place of the Skull.'",
                "Luke 23:46 - 'Father, into your hands I commit my spirit.'"
            ],
            "The Luminous Mysteries": [
                "Matthew 3:16 - 'As soon as Jesus was baptized, he went up out of the water.'",
                "John 2:11 - 'What Jesus did here in Cana of Galilee was the first of the signs.'",
                "Mark 1:15 - 'The kingdom of God has come near. Repent and believe the good news!'",
                "Matthew 17:2 - 'His face shone like the sun, and his clothes became as white as the light.'",
                "Luke 22:19 - 'Do this in remembrance of me.'"
            ]
        }
        self.catechism_references = {
            "The Glorious Mysteries": [
                "CCC 638 - 'The Resurrection of Jesus is the crowning truth of our faith in Christ.'",
                "CCC 659 - 'So then the Lord Jesus, after he had spoken to them, was taken up into heaven.'",
                "CCC 731 - 'On the day of Pentecost when the seven weeks of Easter had come to an end.'",
                "CCC 966 - 'The Assumption of the Blessed Virgin is a singular participation in her Son's Resurrection.'",
                "CCC 971 - 'Mary is honored as the Queen of Heaven and Earth.'"
            ],
            "The Joyful Mysteries": [
                "CCC 490–493 - Discusses Mary’s role and the Immaculate Conception.",
                "CCC 717 - 'John the Baptist is 'the Lord's forerunner, his immediate precursor sent to prepare his way.'",
                "CCC 525 - 'Jesus was born in a humble stable, into a poor family.'",
                "CCC 529 - 'The presentation of Jesus in the temple shows him to be the firstborn son who belongs to the Lord.'",
                "CCC 534 - 'The finding of Jesus in the temple is the only event that breaks the silence of the Gospels about the hidden years of Jesus.'"
            ],
            "The Sorrowful Mysteries": [
                "CCC 612 - 'Christ's agony in the Garden of Gethsemane.'",
                "CCC 572 - 'The Church professes that Jesus suffered death under Pontius Pilate.'",
                "CCC 616 - 'The death of Jesus is part of the mystery of God's plan.'",
                "CCC 618 - 'The cross is the unique sacrifice of Christ, the 'one mediator between God and men.'",
                "CCC 620 - 'Our salvation flows from God's initiative of love for us.'"
            ],
            "The Luminous Mysteries": [
                "CCC 535 - 'The baptism of Jesus is the acceptance and inauguration of his mission as God's suffering Servant.'",
                "CCC 561 - 'The whole of Christ's life was a continual teaching.'",
                "CCC 767 - 'The kingdom of heaven was inaugurated on earth by Christ.'",
                "CCC 554 - 'The Transfiguration gives us a foretaste of Christ's glorious coming.'",
                "CCC 1323 - 'At the Last Supper, our Savior instituted the Eucharistic sacrifice of his Body and Blood.'"
            ]
        }
        self.rosary_structure = [
            "1. Sign of the Cross",
            "2. Apostles' Creed",
            "3. Our Father",
            "4. Three Hail Marys",
            "5. Glory Be",
            "6. First Mystery, Our Father",
            "7. Ten Hail Marys, Glory Be, Fatima Prayer",
            "8. Repeat steps 6-7 for the remaining mysteries",
            "9. Hail Holy Queen",
            "10. Closing Prayer and Sign of the Cross"
        ]

    def load_progress(self):
        try:
            with open("rosary_prayer_progress.json", "r") as file:
                data = json.load(file)
                self.homeless_count = data["homeless_count"]
                self.history = data["history"]
        except FileNotFoundError:
            self.homeless_count = 45252
            self.history = []

    def save_progress(self):
        data = {
            "homeless_count": self.homeless_count,
            "history": self.history
        }
        with open("rosary_prayer_progress.json", "w") as file:
            json.dump(data, file, indent=4)

    def record_prayer(self, date):
        reduction_amount = int(self.homeless_count * self.daily_reduction_rate)
        self.homeless_count -= reduction_amount
        self.homeless_count = max(self.homeless_count, 0)

        self.history.append({"date": date, "remaining_homeless_count": self.homeless_count})
        self.save_progress()

        print(f"✨ Wonderful! You've successfully completed your rosary prayer for {date}. ✨")
        print(f"Together, we reduced the number of people experiencing homelessness by {reduction_amount}!")
        print(f"Remaining homeless count in LA: {self.homeless_count}")
        print("Thank you for your dedication and prayers. 🌟")

    def get_mysteries_for_day(self, day):
        mystery_type = self.mysteries.get(day, "Unknown")
        guidelines = self.mystery_guidelines.get(mystery_type, [])
        print(f"\nToday's Mysteries: {mystery_type}")
        for i, mystery in enumerate(guidelines, 1):
            print(f"{i}. {mystery}")

    def show_spiritual_guidance(self, mystery_type):
        print("\n🌿 Bible Readings 🌿")
        for reading in self.bible_readings.get(mystery_type, []):
            print(reading)
        print("\n📜 Catechism References 📜")
        for reference in self.catechism_references.get(mystery_type, []):
            print(reference)

    def show_rosary_structure(self):
        print("\n🌹 Rosary Prayer Structure 🌹")
        for step in self.rosary_structure:
            print(step)

    def view_progress(self):
        print("📅 Your Prayer Progress 📅")
        if not self.history:
            print("No prayer records found yet. Start today to make an impact!")
        else:
            for record in self.history:
                print(f"Date: {record['date']} | Remaining Homeless Count: {record['remaining_homeless_count']}")
        print(f"Current homeless count in LA: {self.homeless_count}")

    def start(self):
        print("Welcome to the Rosary Prayer Tracker 💖")
        print("Each time you complete your rosary prayer, you help reduce homelessness in Los Angeles.")
        print("Our starting homeless count is 45,252 individuals. Let's pray together to bring that number down!")

        while True:
            print("\nOptions:")
            print("1. Record today's rosary prayer")
            print("2. View my progress")
            print("3. View Rosary Prayer Structure")
            print("4. Exit")

            choice = input("Enter your choice (1, 2, 3, or 4): ")

            if choice == "1":
                date = input("Enter the date (YYYY-MM-DD) for your prayer or press Enter for today: ")
                if not date:
                    date = datetime.now().strftime("%Y-%m-%d")
                day_of_week = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
                mystery_type = self.mysteries.get(day_of_week, "Unknown")
                self.get_mysteries_for_day(day_of_week)
                
                view_guidance = input("Would you like to see Bible readings and Catechism references for today’s mysteries? (yes/no): ")
                if view_guidance.lower() == "yes":
                    self.show_spiritual_guidance(mystery_type)
                
                input("\nAfter reviewing the mysteries, press Enter to record your prayer and see the impact...")
                self.record_prayer(date)
            elif choice == "2":
                self.view_progress()
            elif choice == "3":
                self.show_rosary_structure()
            elif choice == "4":
                print("Thank you for your prayers and support. 🙏 Have a blessed day!")
                break
            else:
                print("Invalid choice. Please try again.")

# Instantiate and start the tracker
tracker = RosaryPrayerTracker()
tracker.start()
