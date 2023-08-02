# helpers.py

from user.models import Profile, Education, Contactdetails, Tsessions, Questionnaire

def get_profile(user):
    try:
        return Profile.objects.select_related('user').get(user=user)
    except Profile.DoesNotExist:
        return None

def profile_complete(profile):
    if profile is None:
        return False
    return (
        profile.surname and
        profile.othernames and
        profile.age and
        profile.image != 'avatar.jpg'
    )

#Get Applicant Education from DB
def get_education(user):
    try:
        return Education.objects.select_related('applicant').get(applicant=user)
    except Education.DoesNotExist:
        return None

#Function for checking whether applicant has Completely filled the Edu Form
def education_complete(education):
    if education is None:
        return False
    return (
        education.qualification and
        education.instition and
        education.graduation
    )

#Get the Applicant contact details from DB
def get_contact_details(user):
    try:
        return Contactdetails.objects.select_related('applicant').get(applicant=user)
    except Contactdetails.DoesNotExist:
        return None
    
#Function for checking whether applicant has filled the Contact Form
def contact_complete(contact):
    if contact is None:
        return False
    return (
        contact.state_origin and
        contact.lga_origin and
        contact.phone and
        contact.home_town and
        contact.village and
        contact.permanent_address
    )
#Get the training session of applicant
def get_training_session(user):
    try:
        return Tsessions.objects.select_related('applicant').get(applicant=user)
    except Tsessions.DoesNotExist:
        return None
#Function for checking whether applicant has a Training Session
def session_complete(trainingsession):
    if trainingsession is None:
        return False
    return (
        trainingsession.training_session and
        trainingsession.training_days
    )
#Get the Applicant Questionnaire Response
def get_question_response(user):
    try:
        return Questionnaire.objects.select_related('applicant').get(applicant=user)
    except Questionnaire.DoesNotExist:
        return None
    
#Function to check if applicant filled the questionnaire
def questionnaire_complete(questionresponse):
    if questionresponse is None:
        return False
    return (
        questionresponse.computer_knowledge and
        questionresponse.own_laptop and
        questionresponse.own_phone and
        questionresponse.browse_internet and
        questionresponse.know_programming and
        questionresponse.learn_night 

    )
