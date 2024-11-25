from django.core.management.base import BaseCommand
from data.models import CarType


class Command(BaseCommand):
    help = 'Populate data'

    def handle(self, *args, **options):
        cars = {
            "Toyota": ["Corolla", "Camry", "RAV4", "Highlander", "Land Cruiser", "Prius", "Yaris", "C-HR", "Tacoma",
                       "Tundra"],
            "Honda": ["Civic", "Accord", "CR-V", "Fit", "Pilot", "HR-V", "Odyssey", "Ridgeline", "Insight", "Passport"],
            "Ford": ["F-150", "Focus", "Mustang", "Explorer", "Escape", "Fiesta", "Edge", "Expedition", "Ranger",
                     "Bronco"],
            "Chevrolet": ["Silverado", "Malibu", "Equinox", "Impala", "Traverse", "Camaro", "Tahoe", "Trailblazer",
                          "Spark", "Colorado"],
            "BMW": ["3 Series", "5 Series", "7 Series", "X3", "X5", "X6", "X7", "M3", "M5", "i3"],
            "Mercedes-Benz": ["C-Class", "E-Class", "S-Class", "GLC", "GLE", "GLA", "GLS", "CLA", "A-Class", "AMG GT"],
            "Audi": ["A3", "A4", "A6", "A8", "Q3", "Q5", "Q7", "Q8", "TT", "RS6"],
            "Volkswagen": ["Golf", "Passat", "Tiguan", "Jetta", "Atlas", "Polo", "Touareg", "Arteon", "ID.4",
                           "Scirocco"],
            "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe", "Accent", "Kona", "Palisade", "Veloster", "Ioniq",
                        "Genesis"],
            "Kia": ["Sorento", "Sportage", "Optima", "Forte", "Telluride", "Soul", "Seltos", "Rio", "Carnival",
                    "Stinger"],
            "Nissan": ["Altima", "Sentra", "Rogue", "Murano", "Maxima", "Pathfinder", "Versa", "Armada", "Kicks",
                       "370Z"],
            "Subaru": ["Impreza", "Outback", "Forester", "Crosstrek", "Legacy", "Ascent", "WRX", "BRZ", "Tribeca",
                       "Baja"],
            "Mazda": ["Mazda3", "Mazda6", "CX-3", "CX-5", "CX-9", "MX-5 Miata", "RX-8", "Mazda2", "B-Series", "CX-30"],
            "Tesla": ["Model S", "Model 3", "Model X", "Model Y", "Roadster", "Cybertruck", "Semi",
                      "Model 2 (upcoming)", "Model A", "Solar Roof"],
            "Lexus": ["RX", "NX", "ES", "GS", "IS", "LS", "GX", "LX", "RC", "UX"],
            "Jeep": ["Wrangler", "Grand Cherokee", "Cherokee", "Compass", "Renegade", "Gladiator", "Patriot", "Liberty",
                     "Commander", "Wagoneer"],
            "Volvo": ["XC40", "XC60", "XC90", "S60", "S90", "V60", "V90", "C40", "V40", "Polestar 2"],
            "Porsche": ["911", "Cayenne", "Panamera", "Macan", "Taycan", "718 Boxster", "718 Cayman", "918 Spyder",
                        "Carrera GT", "Cayman GT4"],
            "Land Rover": ["Range Rover", "Range Rover Sport", "Range Rover Velar", "Discovery", "Discovery Sport",
                           "Defender", "Evoque", "Freelander", "LR3", "LR4"],
            "Ferrari": ["488 GTB", "812 Superfast", "F8 Tributo", "SF90 Stradale", "Portofino", "Roma", "LaFerrari",
                        "California", "458 Italia", "296 GTB"]
        }

        for key, value in cars.items():
            for car in value:
                CarType.objects.create(brand_name=key, model_name=car)

        self.stdout.write(self.style.SUCCESS("Data successfully populated!"))