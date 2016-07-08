# bcpp-interview

Conduct and record In-depth interviews or Focus group discussions.

* Information on potential subjects is preloaded into the PotentialSubjects along with location and locator information.
* Contact with participants for appointment scheduling and reminders is managed and tracked with  `edc-call-manager`.
* Safely stores consent and locator data by encrypting PII with `django-crypto-fields`.
* Imports and displays satellite images for offline use to assist research assistants to locate participants, `edc-map`. 
* Enforces informed consent process before further data collection is permitted using `edc-consent`.
* Records interviews directly on the laptop and manages file storage and linkage to the consented participant/group members.
* Works offline and data can be synchronized with the server later with `edc-sync`.

Uses the python module `sounddevice` for audio recordings.

<B>Important</B>: For now, this is a single user system! The current plan is to deploy multiple instances on offline laptops and not to access over the network as a client/server model. 

### Installation

On MacOSX:

    brew update
    brew install pkg-config libffi libsndfile nginx

On Ubuntu:

    sudo apt-get install libportaudio2 python3-cffi libffi-dev gunicorn nginx

Make a virtualenv (see `virtualenvwrapper`):

    mkvirtualenv venv -p /usr/local/bin/python3 --no-site-packages
    workon venv

Let say you start in a `source` folder, e.g. `~/source`:

    workon venv
    $(venv) cd ~/source
    $(venv) git clone <this repo>
    $(venv) cd ~/bcpp-interview
    $(venv) pip install -r requirements.txt

Or you could `pip install bcpp_interview` into a new project instead of cloning it:

    workon venv
    $(venv) pip install git+https://github.com/botswana-harvard/bcpp-interview@develop#egg=bcpp_interview
    $(venv) pip install -r ~/.virtualenv/venv/lib/python3.5/site-packages/bcpp_interview/requirements.txt

... and then set up a new project:
    
    workon venv
    $(venv) cd ~/source
    $(venv) django-admin startproject server
    $(venv) cd server

... edit the settings file to look like this:

    import os
    from bcpp_interview.settings import *
    from bcpp_interview.settings import INSTALLED_APPS
    
    BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
    KEY_PATH = os.path.join(BASE_DIR.ancestor(1), 'crypto_fields')
    INSTALLED_APPS = INSTALLED_APPS + ['client']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': os.path.join(BASE_DIR.ancestor(1), 'etc', 'default.cnf'),
            },
            'HOST': '',
            'PORT': '',
            'ATOMIC_REQUESTS': True,
        }
    }
    STATIC_ROOT = BASE_DIR.child('static')
    MEDIA_ROOT = BASE_DIR.child('media')
    UPLOAD_FOLDER = os.path.join(MEDIA_ROOT, 'upload')

... create folders:

    cd ~/source/server
    mkdir etc
    mkdir crypto_fields
    mkdir -p server/media/edc_map
    mkdir -p server/media/upload
    touch etc/default.cnf

... a `default.cnf` might look like this:

    [client]
    database = edc
    user = <account>
    password = <password>
    default-character-set = utf8
    init_command = 'SET default_storage_engine=INNODB'

... encryption keys belong in folder `crypto_fields` or some other folder. Keys will be created for you if the folder is empty on the first boot.


For a test environment:

    python manage.py load_test_data
    python manage.py update_categories
    python manage.py createsuperuser2
    
For the production environment:

    # Encryption keys
    # the default KEY_PATH will make the Edc use the keys in the repository.
    # The keys in the repository cannot be used for a production system.
    
    change KEY_PATH in `settings.py`
    
    # Production data    
    # csv file should have same fields as raw data, although only the
    # subject identifier, dob, identity, gender, community, issue, elig_cat are required.
    # Note that the system doesn't actually use the RawData model. So as long as you populate
    # PotentialSubject, SubjectLocator, and SubjectLocation (optional) it will work.
    
    python manage.py load_production_data bcpp_interview.rawdata path/to/my/file.csv
    
    # download images from google maps

    python manage.py fetch_map_images bcpp_interview.subjectlocation 25

### gunicorn / nginx

Activate the virtualenv and install `gunicorn`.

    workon bcpp-interview
    pip install gunicorn
    deactivate
    workon bcpp-interview

In settings set DEBUG=False and update ALLOW_HOSTS accordingly:

    DEBUG = False
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

Collect static files and build `js_reverse` js file:

    cd ~/bcpp-interview
    python manage.py collectstatic
    python manage.py collectstatic_js_reverse

Edit paths in `gunicorn.conf.py` to reflect your installation.

Start `gunicorn` in daemon mode from same folder where `manage.py` resides:

    cd ~/bcpp-interview
    gunicorn -c gunicorn.conf.py bcpp_interview.wsgi --pid ~/bcpp-interview/logs/gunicorn.pid --daemon

This should return nothing. If you get `connection refused`, check your paths in the conf file.:

    curl http://127.0.0.1:9000
    
Now for `nginx`, on macosx, ensure `/usr/local/etc/nginx/nginx.conf` reads from `sites-enabled`:

    http{
        include /usr/local/etc/nginx/sites-enabled/*;

Copy nginx.conf file to `sites-available`. For example:

    cd ~/bcpp-interview
    sudo cp ~/bcpp-interview/nginx.conf /usr/local/etc/nginx/sites-available/bcpp-interview.conf

Edit the paths in the `bcpp-interview.conf` file.

    nano /usr/local/etc/nginx/sites-available/bcpp-interview.conf

Link to `sites-enabled`. (Remove `default` if it is there):

    sudo ln -s /usr/local/etc/nginx/sites-available/bcpp-interview.conf /usr/local/etc/nginx/sites-enabled/bcpp-interview.conf
    
Test `nginx`:
    
    sudo nginx -t
    
If no errors, start `nginx`:

    sudo nginx
    
Browse:

    http://localhost

### Usage
#### Consent potential subjects

* From Home, click "Potential Subjects"
* on the `PotentialSubjects` changelist search for subjects by identity number
* click the "add" button in the consent column for the subject to be consented
* complete and save the consent
* _will return to the `PotentialSubjects` changelist_
* Follow steps for "In-depth Interviews" or "Focus Group Discussions"

####In-depth Interviews

* From Home, click "Potential Subjects"
* You may wish to filter the list "by consent" and/or "by interviewed"   
* Find a consented subject for an IDI  
* Click "IDI", complete a new `In-depth Interview` for the consented subject and save
* _will return to `In-depth Interview` changelist
* On the `In-depth Interview` change_list find the interview and click "Record"
* Follow steps for Recording
* _will return to the `In-depth Interview Recording` page when done_
* Follow steps for Playback and Verification

####Focus Group Discussions

#####Create Focus Group
* From Home, click "Potential Subjects"
* You may wish to filter the list "by consent" and/or "by interviewed"   
* Find the consented subjects to be added to the `FocusGroup`  
* _Note: consented subjects must be in the same category_
* Using the checkboxes on the left, tick each consented subjects to be added
* Select "Create Focus Group" from the "Actions" dropdown and click "Go"
* From one of the focus group members, click "Add" under the Discussion column (_if the discusssion already exists, this will be the disscussion reference number._)

#####Add to existing Focus Group  
* From Home, click "Potential Subjects"
* You may wish to filter the list "by consent" and/or "by interviewed"   
* Find and tick at least one consented subject already in the `FocusGroup` 
* Find and tick the consented subject to be added to the existing `FocusGroup`
* Select "Add to Existing Focus Group" from the "Actions" dropdown and click "Go"
* From one of the focus group members, click "Add" under the Discussion column (_if the discusssion already exists, this will be the disscussion reference number._)

#### Recording
Steps are the same for both `In-depth Interview` and `Focus Group Discussion`
* From Home, click "In-depth Interviews (IDI)" or "Focus Group Discussions"
* On the changelist, find the IDI or FGD and click the RECORD button.
* _on the recording page, a modal will open with a timer and STOP button_
* When the IDI or FGD is over, click the STOP button to stop recording
* _an orange "Wait" alert will appear, wait for the recording to save to file (compressed numpy npz)_
* _once the recording has been saved a green "Success" alert will appear_
* Dismiss the green "Success" alert by clicking the 'X' on the right corning of the green alert
* Click Home on the top left to return to the main menu.

#### Playback and Verification
Steps are the same for both `In-depth InterviewRecording` and `Focus Group Discussion Recording`
* From Home, click "Listen to IDI" or "Listen to FGD"
* Select the recording and click "Play" to listen to the recording
* Click "Stop" to stop playback
* Open the recording and indicate if it has been verified (Yes/No) and if required add a comment
* Save the recording
* Click Home on the top left to return to the main menu.
