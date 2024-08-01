class Blood:
    def __init__(self, haemoglobin, wbc, platelets, mcv, pcv, rbc, mch, mchc, rdw, neutrophils, lymphocytes, monocytes, eosinophils, basophils):
        self.haemoglobin = haemoglobin
        self.wbc = wbc
        self.platelets = platelets
        self.mcv = mcv
        self.pcv = pcv
        self.rbc = rbc
        self.mch = mch
        self.mchc = mchc
        self.rdw = rdw
        self.neutrophils = neutrophils
        self.lymphocytes = lymphocytes
        self.monocytes = monocytes
        self.eosinophils = eosinophils
        self.basophils = basophils

class Human:
    def __init__(self, gender, name, age):
        self.gender = gender
        self.name = name
        self.age = age

class HealthCheck(Blood, Human):
    def __init__(self, haemoglobin, platelets, wbc, mcv, pcv, rbc, mch, mchc, rdw, neutrophils, lymphocytes, monocytes, eosinophils, basophils, gender, age, name):
        Blood.__init__(self, haemoglobin, wbc, platelets, mcv, pcv, rbc, mch, mchc, rdw, neutrophils, lymphocytes, monocytes, eosinophils, basophils)
        Human.__init__(self, gender, name, age)

    def check_male_adult_ranges(self):
        return {
            'haemoglobin': (13.8, 17.2, self.haemoglobin),
            'wbc': (4000, 11000, self.wbc),
            'platelets': (150000, 450000, self.platelets),
            'mcv': (80, 100, self.mcv),
            'pcv': (41, 50, self.pcv),
            'rbc': (4.7, 6.1, self.rbc),
            'mch': (27, 32, self.mch),
            'mchc': (32, 36, self.mchc),
            'rdw': (11.5, 14.5, self.rdw),
            'neutrophils': (40, 60, self.neutrophils),
            'lymphocytes': (20, 40, self.lymphocytes),
            'monocytes': (2, 8, self.monocytes),
            'eosinophils': (1, 4, self.eosinophils),
            'basophils': (0.5, 1, self.basophils)
        }

    def check_female_adult_ranges(self):
        return {
            'haemoglobin': (12.1, 15.1, self.haemoglobin),
            'wbc': (4000, 11000, self.wbc),
            'platelets': (150000, 450000, self.platelets),
            'mcv': (80, 100, self.mcv),
            'pcv': (36, 44, self.pcv),
            'rbc': (4.2, 5.4, self.rbc),
            'mch': (27, 32, self.mch),
            'mchc': (32, 36, self.mchc),
            'rdw': (11.5, 14.5, self.rdw),
            'neutrophils': (40, 60, self.neutrophils),
            'lymphocytes': (20, 40, self.lymphocytes),
            'monocytes': (2, 8, self.monocytes),
            'eosinophils': (1, 4, self.eosinophils),
            'basophils': (0.5, 1, self.basophils)
        }

    def get_ranges(self):
        if self.gender == "male" and self.age > 18:
            return self.check_male_adult_ranges()
        elif self.gender == "female" and self.age > 18:
            return self.check_female_adult_ranges()
        else:
            raise ValueError("Range check for children not implemented")

    def is_fit(self):
        ranges = self.get_ranges()
        for parameter, (low, high, value) in ranges.items():
            if value < low or value > high:
                return False
        return True

    def check_blood_diseases(self):
        messages = []
        ranges = self.get_ranges()
        for parameter, (low, high, value) in ranges.items():
            if value < low:
                if parameter == 'haemoglobin':
                    messages.append(f"Low {parameter} ({value}): You may have anemia.")
                elif parameter == 'platelets':
                    messages.append(f"Low {parameter} ({value}): You may have dengue.")
            elif value > high:
                if parameter == 'haemoglobin':
                    messages.append(f"High {parameter} ({value}): You may have polycythemia.")
                elif parameter == 'platelets':
                    messages.append(f"High {parameter} ({value}): You may have thrombocytosis.")
        return messages

patient = HealthCheck(
    haemoglobin=7.0, wbc=7000, platelets=180000, mcv=90, pcv=42, rbc=5.0, mch=29,
    mchc=34, rdw=12.0, neutrophils=50, lymphocytes=30, monocytes=5, eosinophils=2,
    basophils=0.7, gender='male', name='John Doe', age=25
)

if patient.is_fit():
    print("Report seems all good")
else:
    print(patient.check_blood_diseases())
