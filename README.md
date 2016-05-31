# bcpp-interview

Conduct and record In-depth interviews or Focus group discussions.

* Information on potential subjects is preloaded into the PotentialSubjects 
* Before participating in an IDI or FGD, each subject must complete the Informed Consent. 

Uses the python module `sounddevice` for audio recordings.

Important: For now, this is a single user system! The original plan is to deploy on offline laptops and not to access over the network as client server. 

### Installation

Let say you start in a `source` folder, e.g. `~/source`:

    cd ~/source
    git clone <this repo>
    cd ~/bcpp-interview
    pip install -r requirements.txt
    
For a test environment:

    python manage.py load_test_data
    python manage.py update_categories
    python manage.py createsuperuser2
    
For the production environment:

    change KEY_PATH in `settings.py`
    ...


### Consent potential subjects

* From Home, click "Potential Subjects"
* on the `PotentialSubjects` changelist search for subjects by identity number
* click the "add" button in the consent column for the subject to be consented
* complete and save the consent
* _will return to the `PotentialSubjects` changelist_
* Follow steps for "In-depth Interviews" or "Focus Group Discussions"

###In-depth Interviews

* From Home, click "Potential Subjects"
* You may wish to filter the list "by consent" and/or "by interviewed"   
* Find a consented subject for an IDI  
* Click "IDI", complete a new `In-depth Interview` for the consented subject and save
* _will return to `In-depth Interview` changelist
* On the `In-depth Interview` change_list find the interview and click "Record"
* Follow steps for Recording
* _will return to the `In-depth Interview Recording` page when done_
* Follow steps for Playback and Verification

###Focus Group Discussions

####Create Focus Group
* From Home, click "Potential Subjects"
* You may wish to filter the list "by consent" and/or "by interviewed"   
* Find the consented subjects to be added to the `FocusGroup`  
* _Note: consented subjects must be in the same category_
* Using the checkboxes on the left, tick each consented subjects to be added
* Select "Create Focus Group" from the "Actions" dropdown and click "Go"
* From one of the focus group members, click "Add" under the Discussion column (_if the discusssion already exists, this will be the disscussion reference number._)

####Add to existing Focus Group  
* From Home, click "Potential Subjects"
* You may wish to filter the list "by consent" and/or "by interviewed"   
* Find and tick at least one consented subject already in the `FocusGroup` 
* Find and tick the consented subject to be added to the existing `FocusGroup`
* Select "Add to Existing Focus Group" from the "Actions" dropdown and click "Go"
* From one of the focus group members, click "Add" under the Discussion column (_if the discusssion already exists, this will be the disscussion reference number._)

### Recording
Steps are the same for both `In-depth Interview` and `Focus Group Discussion`
* From Home, click "In-depth Interviews (IDI)" or "Focus Group Discussions"
* On the changelist, find the IDI or FGD and click the RECORD button.
* _on the recording page, a modal will open with a timer and STOP button_
* When the IDI or FGD is over, click the STOP button to stop recording
* _an orange "Wait" alert will appear, wait for the recording to save to file (compressed numpy npz)_
* _once the recording has been saved a green "Success" alert will appear_
* Dismiss the green "Success" alert by clicking the 'X' on the right corning of the green alert
* Click Home on the top left to return to the main menu.

### Playback and Verification
Steps are the same for both `In-depth InterviewRecording` and `Focus Group Discussion Recording`
* From Home, click "Listen to IDI" or "Listen to FGD"
* Select the recording and click "Play" to listen to the recording
* Click "Stop" to stop playback
* Open the recording and indicate if it has been verified (Yes/No) and if required add a comment
* Save the recording
* Click Home on the top left to return to the main menu.
 
###Import Potential Subjects management command

Import a list of potential subjects from CSV of format 'subject_identifier, 'category', 'community', 'region'.

    python manage.py load_csv_data bcpp_interview.potential_subject path_to_file
    
###Update Categories management command

Update categories for the imported potential subjects

    python manage.py update_categories
    
