# WhatsAppChatLogConsolidator
Given some WhatsApp chat log txt and media files, seive out useful data and generate an Excel output. At the end, perform move or copy opreation to tidy things up

main.py : this is where the main loop is. Above the main loop are the functions, roughly corresponding to each column in Excel output and used to get useful data out of the chat logs. Since this can change, the function can be added/substracted and commented out as and when needed.

helper.py : functions that does not pertain to data inside chat logs but necessary for overall working. Things like getting text filenames, filtering date, editing dates, moving-copying and getting text file contents into pandas dataframe.

params.py : levers and buttons to control everything.

