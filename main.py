import os
import helpers as hl
import params as pr
import pandas as pd


def call_status(contents):
    """
    Criteria 1 : 4 photos. i.e. 4 x '.jpg' shows up
    Criteria 2 : GPS location (either gMaps link or live location shared)
    Criteria 3 : Responded? - at least one other user name in chat log
    or
    Criteria 4 : if ###jb is found in chat log then no need criteria 1,2,3
                 if ###sg is found in chat log then still need criteria 1,2,3
    :param contents: dict of string from text file
    :return: dict, key is row, value is either True or False
    """

    call_status_true = 'COMPLETED'
    call_status_false = 'NOT COMPLETED'

    # Check if we pass criteria 1
    crit1 = {row_num: True if contents[row_num]['message'].str.count(pr.MEDIA_FORMATS[0]).sum() >= pr.CRIT1_MIN
            else False for row_num in contents}

    # Check if we pass criteria 2
    crit2 = {row_num: 'YES' if contents[row_num]['message'].str.contains(pr.CRIT2_STR[0]).any() or contents[row_num]['message'].str.contains(pr.CRIT2_STR[1]).any()
            else 'NO' for row_num in contents}

    # Check if we pass criteria 3
    crit3 = {row_num: True if contents[row_num]['username'].nunique() >= pr.CRIT3_NO_USERNAMES
            else False for row_num in contents}

    # Check if we pass criteria 4
    crit4 = {row_num: True if contents[row_num]['message'].str.contains(pr.CRIT4_KW).any()
    else False for row_num in contents}

    output = {row_num: crit4[row_num] if crit4[row_num] else (crit1[row_num] and crit2[row_num] and crit3[row_num]) for row_num in crit4}

    return {row_num: call_status_true if output[row_num] else call_status_false for row_num in output}, (crit1, crit2, crit3, crit4)


def dates_first_last_second(contents):
    """
    First and Last DD/MMM/YYYY HH:00 stamp of ABBA entry in chat log ; Mmm is 1st 3 letter of month
    :param contents: dict of strings from all text files
    :return: string, DD/MMM/YYYY HH:00
    """

    # Init some empty dicts
    output_first = {}
    output_last = {}
    output_second = {}
    # For each chat log dataframe
    for row_num in contents:
        df = contents[row_num]
        unique_names = df['username'].unique()
        company_name = [name for name in unique_names if pr.COMPANY_NAME in name]
        if len(company_name) == 1:
            df_company_name = df.loc[df['username'] == company_name[0]]
            # 1st convo of username 'ABBA ****'
            output_first[row_num] = df_company_name['date'].iloc[0].strftime('%d-%b-%Y %H:%M')
            # Last convo of username 'ABBA ****'
            output_last[row_num] = df_company_name['date'].iloc[-1].strftime('%d-%b-%Y %H:%M')
            # 2nd convo of username 'ABBA ****' , at least 1 day after 1st convo.
            # Here we take 1st entry of all dates larger than 1st convo date.
            try:
                output_second[row_num] = df_company_name['date'][df_company_name['date'].dt.date > df_company_name['date'].iloc[0].date() ].iloc[0].strftime('%d-%b-%Y %H:%M')
            except:
                output_second[row_num] = ''
        if len(company_name) > 1:
            print('>>> More than 1 unique username that starts with ABBA in a chatlog! Expecting only 1.')

    return output_last, output_first, output_second


def vendor_remark(contents):
    """
    if there is CRIT4_KW found, then save content, ending with a period.
    :return: string, ending with a period
    """

    # Keep 'Message' column if the column contains substring pr.CRIT4_KW
    # Then we filter 'Message' column to give us only the row or rows that contains substring CRIT4_KW
    # Then we get only the string within the 1st row
    output = {row_num: contents[row_num]['message'][contents[row_num]['message'].str.contains(pr.CRIT4_KW)].array[0]
                if contents[row_num]['message'].str.contains(pr.CRIT4_KW).any()
                else None for row_num in contents}

    # Perform string op to isolate the content after substring CRIT4_KW
    return {row_num: output[row_num][output[row_num].find(pr.CRIT4_KW) : ].split('\n')[0]+'.'
                if output[row_num] is not None
                else 'NA' for row_num in output}


def file_count(contents):
    """
    A count of all files for a given chat log , Expect minimum 1 (chat log txt)
    :return: int
    """
    output = {}
    for row_num in contents:
        count = 1
        for format in pr.MEDIA_FORMATS:
            count += contents[row_num]['message'].str.count(format).sum()
        output[row_num] = count

    return output


if __name__ == '__main__':

    # Init empty dict for output
    output = {}

    # For each folder
    for path_num in pr.SOURCE_PATHS:
        if os.path.exists(pr.SOURCE_PATHS[path_num]):

            print('\nProcessing SOURCE_PATH ... :', pr.SOURCE_PATHS[path_num])

            # Standardize date formats in all chat logs
            hl.standardize_datetime_formats(hl.get_txt_filenames(pr.SOURCE_PATHS[path_num], fullName=True), pr.SOURCE_PATHS[path_num])

            # Look at chats only between start and end dates
            txts_contents_filtered = hl.filter_date(hl.get_txt_contents(pr.SOURCE_PATHS[path_num]))
            if len(txts_contents_filtered) != len(hl.get_txt_filenames(pr.SOURCE_PATHS[path_num])):
                print('Number of txt files in SOURCE_PATH and filtered dataframe does not match. Check start and end dates in params'
                      ' or date format in chat logs. Exiting ... ')
                break

            # Get col A: filenames, truncated to desired length
            if hl.get_txt_filenames(pr.SOURCE_PATHS[path_num]):
                output['Filename'] = hl.get_txt_filenames(pr.SOURCE_PATHS[path_num], fullName=False, char=pr.FILENAME_CHAR_LENGTH)
            else:
                print('No text files found in SOURCE_PATHS. Exiting ...')
                break

            # Get col B: call_status ; Meanwhile, we also get output of the 4 criteria checks
            output['Call_Status'], criteria_output = call_status(txts_contents_filtered)

            # Get col C,D,E: 1st, last & 2nd call of username ABBA
            # 1st call and 2nd call should be 1 day apart.
            output['Date_CompletedCall'], output['Date_FirstCall'], output['Date_SecondCall'] = dates_first_last_second(txts_contents_filtered)
            for key in output['Call_Status']:
                if output['Call_Status'][key] == 'NOT COMPLETED':
                    output['Date_CompletedCall'][key] = ''

            # Get col F: whether we have pr.CRIT4_KW, i.e. ###CC
            # Instead of True/False, we use YES/NO
            output['Need_Update'] = {key: 'YES' if criteria_output[3][key] is True else 'NO' for key in criteria_output[3]}

            # Get col G: whether we have live location share or location url
            # Instead of True/False, we use YES/NO
            output['GPS_Location'] = {key: 'YES' if criteria_output[2][key] is True else 'NO' for key in criteria_output[2]}

            # Get col H: contents if we have pr.CRIT4_KW
            # Get all content until & exlcude \n , including pr.CRIT4_KW , i.e. ###Blk 123 01-01 \n
            output['Vendor_Remark'] = vendor_remark(txts_contents_filtered)

            # Get col I: including txt file, sum of all files. Expect minimum one
            output['File_Count'] = file_count(txts_contents_filtered)

            # Create output dataframe
            df = pd.DataFrame.from_dict(output)

            # Output to Excel & format.
            try:
                df.to_excel(os.path.join(pr.TARGET_PATHS[path_num], pr.EXCEL_NAME))
                hl.basic_format_excel(os.path.join(pr.TARGET_PATHS[path_num], pr.EXCEL_NAME))
            except:
                print('Something went wrong when processing output Excel. Try closing existing output Excel if any are open')

            # Create folder & move files found in SOURCE_PATHS
            # If copy only is false, then we move files
            if pr.DO_TIDY:
                hl.tidy_my_files(txts_contents_filtered, hl.get_txt_filenames(pr.SOURCE_PATHS[path_num]), path_num, copyOnly=pr.COPY_ONLY)

            print('Completed processing path:', pr.SOURCE_PATHS[path_num], '\n')
        else:
            print('The following path is invalid:', pr.SOURCE_PATHS[path_num], '... Moving on ...\n')

    print('Processing Complete')