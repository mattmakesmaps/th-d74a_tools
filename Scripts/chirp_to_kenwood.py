import csv
import sys
import os

def chirp_to_kenwood(chirp_row):

    chirp_to_kenwood = {
        'Location': ('Ch',),
        'Frequency': ('Rx Freq.','Tx Freq.'),
        'TStep': ('Rx Step','Tx Step'),
        'Offset': ('Offset',),
        'Tone': ('T/CT/DCS',),
        'rToneFreq': ('TO Freq.',),
        'cToneFreq': ('CT Freq.',),
        'DtcsCode': ('DCS Code',),
        'Duplex': ('Shift/Split',),
        'Mode': ('Mode',),
        'Name': ('M.Name',)
    }

    out_row = {}

    for chirp_name, kenwood_names in chirp_to_kenwood.items():
        for kenwood_name in kenwood_names:
            out_row[kenwood_name] = chirp_row[chirp_name]

        # Override value to match expected kenwood syntax.
        if (chirp_name == 'Tone' and chirp_row[chirp_name] == 'Tone'):
            out_row[kenwood_name] = 'T'
    
    return out_row


if __name__ == '__main__':

    source_file_dir = os.path.join(os.curdir, "CHIRP_EXTRACTS")
    source_file_paths = []

    output_file_name = "for_kenwood.hmk"
    output_file_path = os.path.join(os.curdir, output_file_name)

    MODES = ['FM']

    kenwood_header_row = [
        'Ch','Rx Freq.','Rx Step','Offset'
        ,'T/CT/DCS','TO Freq.','CT Freq.','DCS Code'
        ,'Shift/Split','Rev.','L.Out','Mode','Tx Freq.'
        ,'Tx Step','M.Name'
    ]

    kenwood_header_text = """KENWOOD MCP FOR AMATEUR PORTABLE TRANSCEIVER
[Export Software]=MCP-D74 1.03
[Export File Version]=1
[Type]=2
[Language]=English

// Comments
!!Comments=

// Memory Channels
!!Ch,Rx Freq.,Rx Step,Offset,T/CT/DCS,TO Freq.,CT Freq.,DCS Code,Shift/Split,Rev.,L.Out,Mode,Tx Freq.,Tx Step,M.Name
"""

    if os.path.isfile(output_file_path):
        os.remove(output_file_path)

    with open(output_file_path, 'x', newline='\n', encoding='utf-8') as output_handle:

        output_handle.write(kenwood_header_text)

        output_writer = csv.DictWriter(output_handle, kenwood_header_row)

        channel_number = 0

        # Assemble source files
        for source_file in os.listdir(source_file_dir):
            source_file_path = os.path.join(source_file_dir, source_file)
            if os.path.isfile(source_file_path):
                source_file_paths.append(source_file_path)

        # Parse each source file
        for source_file_path in source_file_paths:
            with open(source_file_path) as source_handle:
                chirp_rows = csv.DictReader(source_handle)

                # Convert each row to kenwood format and write.
                for row in chirp_rows:
                    row = chirp_to_kenwood(row)
                    row['Ch'] = channel_number

                    if row['Mode'] in MODES:
                        output_writer.writerow(row)
                        channel_number+=1
