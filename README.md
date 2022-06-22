# WhatsAppChatLogConsolidator
Given some WhatsApp chat log txt and media files, seive out useful data and generate an Excel output. At the end, perform move or copy opreation to tidy things up

This program makes use of Whatstk, Pandas and OpenPyXL.

main.py : this is where the main loop is. Above the main loop are the functions, roughly corresponding to each column in Excel output and used to get useful data out of the chat logs. Since this can change, the function can be added/substracted and commented out as and when needed.

helper.py : functions that does not pertain to data inside chat logs but necessary for overall working. Things like getting text filenames, filtering date, editing dates, moving-copying and getting text file contents into pandas dataframe.

params.py : levers and buttons to control everything.

Take for example column "File_Count" in Excel output: This corresponds to the number of files exchanged in the chat log. Function file_count() in main takes a dataframe of chat log contents, and increments a count if any of the substring in params' MEDIA_FORMAT is found. 

Column "Call_Status" is the most complicated in this use case: involving checking if there were at least 4 media files exchanged, whether a location was shared, whether someone responded in the chat log and whether a super user specified keyword (in this case ###CC) was found. Call is considered 'COMPLETED' if super user specified keyword was found, regardless of whether the other 3 criteria is fulfilled. If not found, then all 3 other criteria must be fulfilled to consider the call 'COMPLETED'. Else, it is 'NOT COMPLETED'
