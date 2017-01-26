from django.db import models


def set_flag_priority(self, priority):
    self.flag_priority = priority
    return self

def set_notice_priority(self, priority):
    self.notice_priority = priority
    return self

models.BooleanField.set_flag_priority = set_flag_priority
models.BooleanField.set_notice_priority = set_notice_priority


class InterceptionRecord(models.Model):
    irf_number = models.CharField(max_length=20, unique=True)
    date_time_of_interception = models.DateTimeField()

    drugged_or_drowsy = models.BooleanField(default=False).set_flag_priority(50)
    meeting_someone_across_border = models.BooleanField(default=False).set_flag_priority(16)
    seen_in_last_month_in_nepal = models.BooleanField(default=False).set_flag_priority(20)
    traveling_with_someone_not_with_her = models.BooleanField(default=False).set_flag_priority(8)
    wife_under_18 = models.BooleanField(default=False).set_flag_priority(7)
    married_in_past_2_weeks = models.BooleanField(default=False).set_flag_priority(25)
    married_in_past_2_8_weeks = models.BooleanField(default=False).set_flag_priority(28)
    less_than_2_weeks_before_eloping = models.BooleanField(default=False).set_flag_priority(18)
    between_2_12_weeks_before_eloping = models.BooleanField(default=False).set_flag_priority(24)
    caste_not_same_as_relative = models.BooleanField(default=False).set_flag_priority(6)
    caught_in_lie = models.BooleanField(default=False).set_flag_priority(14)

    # Where are you going, and for what?
    doesnt_know_going_to_india = models.BooleanField(default=False).set_flag_priority(50) # Should be 1 but not currently in use
    running_away_over_18 = models.BooleanField(default=False).set_flag_priority(23)
    running_away_under_18 = models.BooleanField(default=False).set_flag_priority(5)
    going_to_gulf_for_work = models.BooleanField(default=False).set_flag_priority(50)
    no_address_in_india = models.BooleanField(default=False).set_flag_priority(27)
    no_company_phone = models.BooleanField(default=False).set_flag_priority(22)
    no_appointment_letter = models.BooleanField(default=False).set_flag_priority(31)
    valid_gulf_country_visa = models.BooleanField(default=False).set_flag_priority(50) # Should be 13 but not currently in use
    passport_with_broker = models.BooleanField(default=False).set_flag_priority(11)
    job_too_good_to_be_true = models.BooleanField(default=False).set_flag_priority(10)
    not_real_job = models.BooleanField(default=False).set_flag_priority(4)
    couldnt_confirm_job = models.BooleanField(default=False).set_flag_priority(30)

    no_bags_long_trip = models.BooleanField(default=False).set_flag_priority(21)
    shopping_overnight_stuff_in_bags = models.BooleanField(default=False).set_flag_priority(12)

    no_enrollment_docs = models.BooleanField(default=False).set_flag_priority(26)
    doesnt_know_school_name = models.BooleanField(default=False).set_flag_priority(9)
    no_school_phone = models.BooleanField(default=False).set_flag_priority(15)
    not_enrolled_in_school = models.BooleanField(default=False).set_flag_priority(3)

    reluctant_treatment_info = models.BooleanField(default=False).set_flag_priority(29)
    no_medical_documents = models.BooleanField(default=False).set_flag_priority(19)
    fake_medical_documents = models.BooleanField(default=False).set_flag_priority(2)
    no_medical_appointment = models.BooleanField(default=False).set_flag_priority(17)

    doesnt_know_villiage_details = models.BooleanField(default=False).set_flag_priority(50)
    reluctant_villiage_info = models.BooleanField(default=False).set_flag_priority(50)
    reluctant_family_info = models.BooleanField(default=False).set_flag_priority(50)
    refuses_family_info = models.BooleanField(default=False).set_flag_priority(50)
    under_18_cant_contact_family = models.BooleanField(default=False).set_flag_priority(50)
    under_18_family_doesnt_know = models.BooleanField(default=False).set_flag_priority(50)
    under_18_family_unwilling = models.BooleanField(default=False).set_flag_priority(50)
    over_18_family_doesnt_know = models.BooleanField(default=False).set_flag_priority(50)
    over_18_family_unwilling = models.BooleanField(default=False).set_flag_priority(50)

    # What was the sign that made you stop the girl for questioning? (check all that apply below)

    # Manner
    noticed_hesitant = models.BooleanField(default=False).set_notice_priority(6)
    noticed_nervous_or_afraid = models.BooleanField(default=False).set_notice_priority(2)
    noticed_hurrying = models.BooleanField(default=False).set_notice_priority(7)
    noticed_drugged_or_drowsy = models.BooleanField(default=False).set_notice_priority(1)

    # Attire
    noticed_new_clothes = models.BooleanField(default=False).set_notice_priority(14)
    noticed_dirty_clothes = models.BooleanField(default=False).set_notice_priority(15)
    noticed_carrying_full_bags = models.BooleanField(default=False).set_notice_priority(13)
    noticed_village_dress = models.BooleanField(default=False).set_notice_priority(3)

    # Appearance
    noticed_indian_looking = models.BooleanField(default=False).set_notice_priority(8)
    noticed_typical_village_look = models.BooleanField(default=False).set_notice_priority(9)
    noticed_looked_like_agent = models.BooleanField(default=False).set_notice_priority(10)
    noticed_caste_difference = models.BooleanField(default=False).set_notice_priority(50)
    noticed_young_looking = models.BooleanField(default=False).set_notice_priority(4)

    # Action
    noticed_waiting_sitting = models.BooleanField(default=False).set_notice_priority(11)
    noticed_walking_to_border = models.BooleanField(default=False).set_notice_priority(12)
    noticed_roaming_around = models.BooleanField(default=False).set_notice_priority(17)
    noticed_exiting_vehicle = models.BooleanField(default=False).set_notice_priority(19)
    noticed_heading_to_vehicle = models.BooleanField(default=False).set_notice_priority(18)
    noticed_in_a_vehicle = models.BooleanField(default=False).set_notice_priority(22)
    noticed_in_a_rickshaw = models.BooleanField(default=False).set_notice_priority(5)
    noticed_in_a_cart = models.BooleanField(default=False).set_notice_priority(16)
    noticed_carrying_a_baby = models.BooleanField(default=False).set_notice_priority(20)
    
    
    trafficker_taken_into_custody = models.CharField(max_length=20, null=True, blank=True)

    HOW_SURE_TRAFFICKING_CHOICES = [
        (1, '1 - Not at all sure'),
        (2, '2 - Unsure but suspects it'),
        (3, '3 - Somewhat sure'),
        (4, '4 - Very sure'),
        (5, '5 - Absolutely sure'),
    ]
    how_sure_was_trafficking = models.IntegerField(choices=HOW_SURE_TRAFFICKING_CHOICES)

    def get_highest_flag_priority(self):
        highest = 50
        for field in self._meta.fields:
            if type(field) == models.BooleanField:
                value = getattr(self, field.name)
                if value is True:
                    if hasattr(field, 'flag_priority') and field.flag_priority<highest:
                        highest = field.flag_priority
        return highest

    def get_highest_notice_priority(self):
        highest = 50
        for field in self._meta.fields:
            if type(field) == models.BooleanField:
                value = getattr(self, field.name)
                if value is True:
                    if hasattr(field, 'notice_priority') and field.notice_priority<highest:
                        highest = field.notice_priority
        return highest
