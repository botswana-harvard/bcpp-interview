# bcpp-interview

Record and interview with a consented subject or record a group discussion with consented subjects.

Uses the python module `sounddevice`.

Note: consented subjects must have been previously consented in BCPP


###Interview

* consent a subject
* complete a new `Interview` for the consented subject and save
* in the `Interview` change_list select the interview and choose the "Start recording interview" action
* on the recording page, click the RECORD button.
* ''on the recording page, a modal will open with a timer and STOP button''
* when the interview is over, click the STOP button
* ''an alert will appear, wait for the recording to save to file (compressed numpy npz)''
* ''once saved, an SUCCESS alert will appear''
* dismiss the alert by clicking the 'X'
* ''a newly created `InterviewRecording` will open''
* on the `InterviewRecording` indicate that the consented subject agrees the recording may be used for analysis
* on the `InterviewRecording` indicate additional comments of interest for analysis
* save the `InterviewRecording`
 

###Group Discussion

same as above except

* consent a number of subjects
* create a `SubjectGroup` and add each consented subject
* create a `GroupDiscussion` and select the newly create `SubjectGroup`
* in the `GroupDiscussion` change_list select the group discussion and choose the "Start recording interview" action
...

###Import subjects management command

* import a list of potential subjects from CSV of format 'subject_identifier, 'category', 'community', 'region'.
