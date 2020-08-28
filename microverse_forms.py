import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

selection = ''
system_options = {
    'flags': {
        'auto_complete': False
    },
    'has_flags': False,
    'options': ''
}


def has_flags():
    if sys.argv:
        system_options['has_flags'] = True


def flag_parser():
    if not system_options['has_flags']:
        return
    flags = str(sys.argv)
    options = system_options['options']
    for flag in flags:
        if flag == '-a' or flag == '--auto':
            print('flag -a')
            system_options['flags']['auto_complete'] = True


def auto_complete():
    print('Auto-complete is on, setting all radio options to default.')
    return options['default']


def reset():
    driver.refresh()


def pickOption(selection, id=""):
    return driver.find_element_by_id(f'{selection}{id}')


def form_group_radio(input_text, selection, options):
    if system_options['flags']['auto_complete']:
        user_input = auto_complete(options)
    else:
        user_input = input(input_text).strip()
    if user_input in options:
        id = options[user_input]
        selection = pickOption(selection, id)
    else:
        id = options[options['default']]
        selection = pickOption(selection, id)
        print(f'Choosing default: {options["default"]}')
    selection.click()


print(sys.argv)


URL = 'https://dashboard.microverse.org'
EMAIL = 'youremail'
PASSWORD = 'yourpass'
driver = webdriver.Firefox()

driver.get(URL)
time.sleep(10)
inputs = driver.find_elements_by_tag_name('input')
login_button = driver.find_element_by_tag_name('button')

inputs[0].send_keys(EMAIL)
inputs[1].send_keys(PASSWORD)
login_button.click()

time.sleep(10)

#forms_page = driver.find_element_by_class_name('ca-sidebar-forms')
forms_page = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'ca-sidebar-forms'))
)
forms_page.click()

time.sleep(5)
selection = ''
all_forms = driver.find_elements_by_class_name('form-title')
user_input = input('Which form would you like? [daily, mob, peer]: ').strip()

has_flags()
flag_parser()

if (user_input == 'daily'):
    all_forms[1].click()
    time.sleep(3)

    # Standup Acheived Goals
    user_input = input(
        'Did you achieve your goals from yesterday? [all, some, none]')
    choices = driver.find_elements_by_tag_name('option')
    options = {
        'all': 0,
        'some': 1,
        'none': 2,
        'default': 'all'
    }
    id = options[user_input]
    choices[id].click()

    # Standup Upsides
    user_input = input('What went well today?')
    text_area = driver.find_element_by_id('standup_upsides')
    text_area.send_keys(user_input)

    # Blockers
    no_blockers = driver.find_element_by_id('blockers_none')
    no_blockers.click()

    # Goals
    goal_one = driver.find_element_by_id('goals_1')
    goal_two = driver.find_element_by_id(('goals_2'))
    goal_three = driver.find_element_by_id('goals_3')

    user_input_goal_one = input('What is your first goal of the day?')
    user_input_goal_two = input('What is your second goal of the day?')
    user_input_goal_three = input('What is your third goal of the day?')

    goal_one.send_keys(user_input_goal_one)
    goal_two.send_keys(user_input_goal_two)
    goal_three.send_keys(user_input_goal_three)

    # Stand Up Goals Confidence
    user_input = input('What will you do to ensure you reach your goals?')
    text_area = driver.find_element_by_id('standup_goals_confidence')
    text_area.send_keys(user_input)

    # Overall Motivation
    input_text = 'What was your overall motivation? [perfect, good, decent, bad]'
    selection = 'motivation_'
    options = {
        'perfect': '0',
        'good': '1',
        'decent': '2',
        'bad': '3',
        'default': 'perfect'
    }
    form_group_radio(input_text, selection, options)

    # Submit
    user_input = input('Submit form? [yes, no]')
    if user_input == 'yes':
        submit_button = driver.find_element_by_class_name('btn-murple')
        submit_button.click()
    elif user_input == 'no':
        reset()


elif (user_input == 'peer'):
    all_forms[2].click()
    time.sleep(5)
    id = 0

    role = input(
        'What was your role during this morning session? [master, presenter, reviewer]').strip()
    if(role == 'master'):
        id = 0
    elif(role == 'presenter'):
        id = 1
    elif(role == 'reviewer'):
        id = 2
    else:
        id = 2
        print('Choosing default: reviewer')

    selection = pickOption('role_', id)
    selection.click()

    loud = input('Did the speaker speak loud enough? [yes, no]').strip()
    if(loud == 'yes'):
        id = 0
    elif(loud == 'no'):
        id = 1
    else:
        id = 0

    selection = pickOption('loud_enough_', id)
    selection.click()

    wording = input(
        "How easy was it to understand presenter's wording? [0 - 5]").strip()
    choices = ['1', '2', '3' '4', '5']
    if wording in choices:
        selection = pickOption('wording_rating_', wording)
    else:
        selection = pickOption('wording_rating_', '5')
        print('Choosing default: 5')
    selection.click()

    clear_description = input(
        'Was there a clear descriptiton of the project context? [perfect, good, decent, bad]').strip()
    choices = {
        'perfect': '0',
        'good': '1',
        'decent': '2',
        'bad': '3'
    }
    if choices[clear_description]:
        selection = pickOption(
            'project_context_description_', choices[clear_description])
    else:
        selection = pickOption('project_context_description_', '0')
        print('Choosing default: perfect')

    selection.click()

    clear_presentation = input(
        'Was the presentation clear? [perfect, good, decent, bad]').strip()
    if choices[clear_presentation]:
        id = choices[clear_presentation]
        selection = pickOption('code_description_', id)
    else:
        id = '0'
        selection = pickOption('code_description_', id)
        print('Choosing default: perfect')

    selection.click()

    feedback = input(
        'How was the presenters response to feedback? [perfect, good, decent, bad]').strip()
    if choices[feedback]:
        id = choices[feedback]
        selection = pickOption('feedback_response_', id)
    else:
        id = '0'
        selection = pickOption('feedback_response_', id)
        print('Choosing default: perfect')

    selection.click()

    link = input('Input Github issue link.: ')
    selection = pickOption('code_review_session_github_link')
    selection.click()

    happy = input(
        'How would you rate this morning session? [perfect, good, decent, bad]')
    if choices[happy]:
        id = choices[happy]
        selection = pickOption('overall_rating_', id)
    else:
        id = '0'
        selection = pickOption('overall_rating_', id)
        print('Choosing default: perfect')

    selection.click()

    optional = input('Anything else to add (optional)?')
    if optional:
        selection = pickOption('code_review_session_comments')
        selection.send_keys(optional)

    submit = driver.find_element_by_class_name('btn-murple')
    submit.click()

elif (user_input == 'mob'):
    all_forms[3].click()
    time.sleep(3)
    id = 0

    # Role
    input_text = 'What was your role during this morning session? [master, presenter, reviewer]'
    selection = 'role_'
    options = {
        'master': '0',
        'presenter': '1',
        'reviewer': '2',
        'default': 'reviewer'
    }
    form_group_radio(input_text, selection, options)

    # Loudness
    input_text = 'Was the presenter loud enough? [yes, no]'
    selection = 'loud_enough_'
    options = {
        'yes': '0',
        'no': '1',
        'default': 'yes'
    }
    form_group_radio(input_text, selection, options)

    # Presenter performance
    input_text = "How easy was it to understand the presenter's wording? [0 - 5]"
    selection = 'wording_rating_'
    options = {
        '0': '0',
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5',
        'default': '5'
    }
    form_group_radio(input_text, selection, options)

    # Writing Code
    input_text = 'Was the presenter fluent in writing code in real-time? [perfect, decent, bad]'
    selection = 'real_time_code_'
    options = {
        'perfect': '0',
        'decent': '1',
        'bad': 'bad',
        'default': 'perfect'
    }
    form_group_radio(input_text, selection, options)

    # Real Life Help
    input_text = 'Did the presenter use real-life help from other students? [yes, no]'
    selection = 'real_life_help_'
    options = {
        'yes': '0',
        'no': '1',
        'default': 'yes'
    }
    form_group_radio(input_text, selection, options)

    # Ask For Help
    input_text = 'Was the presenter not afraid to ask for help? [yes, no, ns (not stuck)]'
    selection = 'ask_for_help_'
    options = {
        'yes': '0',
        'no': '1',
        'ns': '2',
        'default': 'ns'
    }
    form_group_radio(input_text, selection, options)

    # Solution With Example
    input_text = 'Did the presenter try solutions with examples? [yes, no]'
    selection = 'solution_with_examples_'
    options = {
        'yes': '0',
        'no': '1',
        'default': 'yes'
    }
    form_group_radio(input_text, selection, options)

    # Solution Efficiency
    input_text = 'Did the presenter remember solution efficency? [yes, no]'
    selection = 'solution_efficiency_'
    options = {
        'yes': '0',
        'no': '1',
        'default': 'yes'
    }
    form_group_radio(input_text, selection, options)

    # Feedback Response
    input_text = 'How did the presenter respond to feedback? [perfect, decent, bad]'
    selection = 'feedback_response_'
    options = {
        'perfect': '0',
        'decent': '1',
        'bad': '2',
        'default': 'perfect'
    }
    form_group_radio(input_text, selection, options)

    # Coding Challenge Name
    input_text = input('Enter coding challenge name: [ex: Decode Ways]')
    selection = 'algorithms_session_coding_challenge_id'
    element = driver.find_element_by_id(selection)
    element.click()
    element.send_keys(input_text)
    options = driver.find_elements_by_tag_name('option')

    # Overall Rating

    input_text = input(
        'How would you rate this mornings session? [perfect, good, decent, bad]')
    selection = 'overall_rating_'
    options = {
        'perfect': '0',
        'good': '1',
        'decent': '2',
        'bad': '3',
        'default': 'perfect'
    }
    form_group_radio(input_text, selection, options)

    # Optional Comments
    optional = driver.find_element_by_id('algorithms_session_comments')
    user_input = input('Do you have any additional comments?')
    if user_input != '':
        optional.send_keys(user_input)

    submit_button = driver.find_element_by_class_name('btn-murple')
    submit_button.click()
    print('Mob programming form submitted!')

driver.close()
