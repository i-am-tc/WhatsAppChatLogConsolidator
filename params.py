# Where to read chat logs and media files
# LOCAL_PATHS and TARGET_PATHS should match:
# What we have in index 0 of local will be moved to index 0 of target.
# What we have in index 1 of local will be moved to index 1 of target.
# Note 1: "./" basically means current directory that script in situated
# Note 2: You can add Windows absolute paths , i.e. C:\Users\sar02\Desktop ; for Python, replace Window's "\" with "/"
SOURCE_PATHS = {
0: './Input_Sample'
}

# Where to move chat logs and media files to.
TARGET_PATHS = {
0: './'
}

# Supported date formats
DATE_FORMATS = ['%d/%m/%y, %H:%M - %name:', '%d/%m/%y, %H:%M \S\S - %name:',
                '%m/%d/%Y, %H:%M - %name:', '%m/%d/%Y, %H:%M \S\S - %name:',
                '%d.%m.%y, %H:%M - %name:', '%d.%m.%y, %H:%M \S\S - %name:',
                '%m.%d.%Y, %H:%M - %name:', '%m.%d.%Y, %H:%M \S\S - %name:']
# For selection of dates within a long chat log.
# Expects a YYYY-MM-DD format.
START_DATE = '2022-04-01'
END_DATE = '2022-04-30'

#Company Name
COMPANY_NAME = 'ABBA'

# Media format to check for
MEDIA_FORMATS = ('.jpg', '.opus', '.webp')

# Criteria 1 : Minimum number of photos we want to see in a chat log. If 4 photos. i.e. 4 x '.jpg' shows up
# Criteria 2 : String to search for to confirm we have GPS location in a chat log (either gMaps link or live location shared)
# Criteria 3 : How many unique usernames we have? A proxy of whether we have ongoign convo - at least one other user name in chat log
# Criteria 4 : if ###jb is found in chat log then no need criteria 1,2,3 ; if ###sg is found in chat log then still need criteria 1,2,3
CRIT1_MIN = 4
CRIT2_STR = ('live location shared', 'https://maps.google.com')
CRIT3_NO_USERNAMES = 2
CRIT4_KW = '###CC'

# Filename to retain for filename column in output Excel
FILENAME_CHAR_LENGTH = 60

# Excel parameters
EXCEL_NAME = 'output.xlsx'
HIDE_COL_START = 'K'
HIDE_COL_END = 'XFD'
COL_NAME_COLOUR = '00FFFF00' # See here for more colors: https://is.gd/9XoduK

# If DO_TIDY = False, we only generate output excel. No tidying is done.
DO_TIDY = True

# Tidy my files parameters
# If copy only is false, then we MOVE files
# If copy only is true, then we WILL NOT move files but copy-tidy the files
COPY_ONLY = True

# WARNING: once we execute with COPY_ONLY = FALSE, it will move files.
# Once files move, it will not be possible to build output again.
# The logic requires that all txt and media files are in the directory stipulated in SOURCE_PATHS
# Use with COPY_ONLY = True if unsure!