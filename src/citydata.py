# citydata.py

# The packed city record format:
#
# \x0a\x4b\x61\x62\x75\x6c\x01\x68\x00\x8c\
#
#  ^-^-------------------------------------- The city record size in bytes (e.g. 10)
#      ^-----------------^-------------------The city name (e.g. "Kabul")
#                          ^-----^-----------The x coordinate (e.g. 360)
#                                  ^-----^-- The y coordinate (e.g. 140)

numOfCities= 187

citydataBytes= b'\
\x0a\x4b\x61\x62\x75\x6c\x01\x67\x00\x8e\
\x0b\x54\x69\x72\x61\x6e\x65\x01\x10\x00\x7f\
\x0c\x41\x6c\x67\x69\x65\x72\x73\x00\xf2\x00\x89\
\x15\x41\x6e\x64\x6f\x72\x72\x61\x20\x6c\x61\x20\x56\x65\x6c\x6c\x61\x00\xef\x00\x7c\
\x0b\x4c\x75\x61\x6e\x64\x61\x01\x04\x00\xe2\
\x10\x57\x65\x73\x74\x20\x49\x6e\x64\x69\x65\x73\x00\x80\x00\xb1\
\x11\x42\x75\x65\x6e\x6f\x73\x20\x41\x69\x72\x65\x73\x00\x83\x01\x1b\
\x0c\x59\x65\x72\x65\x76\x61\x6e\x01\x3c\x00\x81\
\x0f\x4f\x72\x61\x6e\x6a\x65\x73\x74\x61\x64\x00\x71\x00\xba\
\x0d\x43\x61\x6e\x62\x65\x72\x72\x61\x01\xf5\x01\x18\
\x0b\x56\x69\x65\x6e\x6e\x61\x01\x0a\x00\x6e\
\x09\x42\x61\x6b\x75\x01\x45\x00\x81\
\x0b\x4e\x61\x73\x73\x61\x75\x00\x64\x00\xa1\
\x0b\x4d\x61\x6e\x61\x6d\x61\x01\x46\x00\x9f\
\x0a\x44\x68\x61\x6b\x61\x01\x8d\x00\xa4\
\x0f\x42\x72\x69\x64\x67\x65\x74\x6f\x77\x6e\x00\x84\x00\xb9\
\x0a\x4d\x69\x6e\x73\x6b\x01\x1d\x00\x61\
\x0d\x42\x72\x75\x73\x73\x65\x6c\x73\x00\xf4\x00\x68\
\x0d\x42\x65\x6c\x6d\x6f\x70\x61\x6e\x00\x51\x00\xb1\
\x0f\x50\x6f\x72\x74\x6f\x20\x4e\x6f\x76\x6f\x00\xf1\x00\xc6\
\x0c\x54\x68\x69\x6d\x70\x68\x75\x01\x8c\x00\x9d\
\x0b\x4c\x61\x20\x50\x61\x7a\x00\x74\x00\xf1\
\x0d\x53\x61\x72\x61\x6a\x65\x76\x6f\x01\x0d\x00\x79\
\x0d\x47\x61\x62\x6f\x72\x6f\x6e\x65\x01\x1a\x01\x02\
\x0d\x42\x72\x61\x73\x69\x6c\x69\x61\x00\x99\x00\xf0\
\x0e\x52\x6f\x61\x64\x20\x54\x6f\x77\x6e\x00\x7b\x00\xaf\
\x15\x42\x61\x6e\x64\x61\x72\x20\x53\x65\x72\x69\x20\x42\x65\x67\x2e\x01\xb9\x00\xc9\
\x0a\x53\x6f\x66\x69\x61\x01\x16\x00\x7c\
\x10\x4f\x75\x61\x67\x61\x64\x6f\x75\x67\x6f\x75\x00\xeb\x00\xbb\
\x0e\x42\x75\x6a\x75\x6d\x62\x75\x72\x61\x01\x21\x00\xd8\
\x0f\x50\x68\x6e\x6f\x6d\x20\x50\x65\x6e\x68\x01\xa6\x00\xbc\
\x0c\x59\x61\x6f\x75\x6e\x64\x65\x01\x01\x00\xcb\
\x0b\x4f\x74\x74\x61\x77\x61\x00\x67\x00\x75\
\x0a\x50\x72\x61\x69\x61\x00\xc4\x00\xb5\
\x10\x47\x65\x6f\x72\x67\x65\x20\x54\x6f\x77\x6e\x00\x5d\x00\xad\
\x0b\x42\x61\x6e\x67\x75\x69\x01\x0e\x00\xca\
\x0e\x4e\x27\x44\x6a\x61\x6d\x65\x6e\x61\x01\x07\x00\xbb\
\x0d\x53\x61\x6e\x74\x69\x61\x67\x6f\x00\x70\x01\x14\
\x0c\x42\x65\x69\x6a\x69\x6e\x67\x01\xbb\x00\x82\
\x0b\x42\x6f\x67\x6f\x74\x61\x00\x6a\x00\xca\
\x0b\x4d\x6f\x72\x6f\x6e\x69\x01\x39\x00\xe8\
\x10\x42\x72\x61\x7a\x7a\x61\x76\x69\x6c\x6c\x65\x01\x08\x00\xda\
\x0d\x53\x61\x6e\x20\x4a\x6f\x73\x65\x00\x58\x00\xc0\
\x11\x59\x61\x6d\x6f\x75\x73\x73\x6f\x75\x6b\x72\x6f\x00\xe4\x00\xc6\
\x0b\x5a\x61\x67\x72\x65\x62\x01\x09\x00\x74\
\x0b\x48\x61\x76\x61\x6e\x61\x00\x5b\x00\xa5\
\x0c\x4e\x69\x63\x6f\x73\x69\x61\x01\x28\x00\x8c\
\x0b\x50\x72\x61\x67\x75\x65\x01\x06\x00\x69\
\x0d\x4b\x69\x6e\x73\x68\x61\x73\x61\x01\x08\x00\xda\
\x0f\x43\x6f\x70\x65\x6e\x68\x61\x67\x65\x6e\x01\x03\x00\x5c\
\x0d\x44\x6a\x69\x62\x6f\x75\x74\x69\x01\x38\x00\xbd\
\x0b\x52\x6f\x73\x65\x61\x75\x00\x80\x00\xb5\
\x12\x53\x61\x6e\x74\x6f\x20\x44\x6f\x6d\x69\x6e\x67\x6f\x00\x72\x00\xaf\
\x09\x44\x69\x6c\x69\x01\xcb\x00\xe2\
\x0a\x51\x75\x69\x74\x6f\x00\x62\x00\xd2\
\x0a\x43\x61\x69\x72\x6f\x01\x24\x00\x97\
\x11\x53\x61\x6e\x20\x53\x61\x6c\x76\x61\x64\x6f\x72\x00\x4f\x00\xb8\
\x0b\x4d\x61\x6c\x61\x62\x6f\x00\xfc\x00\xcc\
\x0b\x41\x73\x6d\x61\x72\x61\x01\x31\x00\xb5\
\x0c\x54\x61\x6c\x6c\x69\x6e\x6e\x01\x18\x00\x51\
\x10\x41\x64\x64\x69\x73\x20\x41\x62\x61\x62\x61\x01\x31\x00\xc1\
\x0c\x53\x74\x61\x6e\x6c\x65\x79\x00\x84\x01\x3e\
\x0d\x54\x6f\x72\x73\x68\x61\x76\x6e\x00\xe1\x00\x49\
\x0d\x48\x65\x6c\x73\x69\x6e\x6b\x69\x01\x19\x00\x4e\
\x0a\x50\x61\x72\x69\x73\x00\xf1\x00\x6d\
\x0c\x43\x61\x79\x65\x6e\x6e\x65\x00\x91\x00\xc8\
\x0f\x4c\x69\x62\x72\x65\x76\x69\x6c\x6c\x65\x00\xfd\x00\xd2\
\x0b\x42\x61\x6e\x6a\x75\x6c\x00\xd0\x00\xb9\
\x0d\x54\x27\x62\x69\x6c\x69\x73\x69\x01\x3c\x00\x7e\
\x0b\x42\x65\x72\x6c\x69\x6e\x01\x04\x00\x64\
\x0a\x41\x63\x63\x72\x61\x00\xed\x00\xc8\
\x0b\x41\x74\x68\x65\x6e\x73\x01\x17\x00\x87\
\x09\x4e\x75\x75\x6b\x00\x92\x00\x43\
\x10\x42\x61\x73\x73\x65\x2d\x54\x65\x72\x72\x65\x00\x80\x00\xb3\
\x0e\x47\x75\x61\x74\x65\x6d\x61\x6c\x61\x00\x4d\x00\xb6\
\x13\x53\x74\x2e\x20\x50\x65\x74\x65\x72\x20\x50\x6f\x72\x74\x00\xe9\x00\x6b\
\x0c\x43\x6f\x6e\x61\x6b\x72\x79\x00\xd5\x00\xc0\
\x0b\x42\x69\x73\x73\x61\x75\x00\xd2\x00\xbc\
\x0f\x47\x65\x6f\x72\x67\x65\x74\x6f\x77\x6e\x00\x86\x00\xc6\
\x13\x50\x6f\x72\x74\x2d\x61\x75\x2d\x50\x72\x69\x6e\x63\x65\x00\x6d\x00\xae\
\x06\x20\x01\x70\x01\x42\
\x10\x54\x65\x67\x75\x63\x69\x67\x61\x6c\x70\x61\x00\x53\x00\xb7\
\x0d\x42\x75\x64\x61\x70\x65\x73\x74\x01\x0f\x00\x70\
\x0e\x52\x65\x79\x6b\x6a\x61\x76\x69\x6b\x00\xc7\x00\x43\
\x0e\x4e\x65\x77\x20\x44\x65\x6c\x68\x69\x01\x76\x00\x9a\
\x0c\x4a\x61\x6b\x61\x72\x74\x61\x01\xaa\x00\xde\
\x0b\x54\x65\x68\x72\x61\x6e\x01\x48\x00\x8b\
\x0c\x42\x61\x67\x68\x64\x61\x64\x01\x3c\x00\x90\
\x0b\x44\x75\x62\x6c\x69\x6e\x00\xe2\x00\x61\
\x0e\x4a\x65\x72\x75\x73\x61\x6c\x65\x6d\x00\xaf\x00\x93\
\x09\x52\x6f\x6d\x65\x01\x03\x00\x7e\
\x0d\x4b\x69\x6e\x67\x73\x74\x6f\x6e\x00\x65\x00\xaf\
\x0a\x41\x6d\x6d\x61\x6e\x01\x2c\x00\x94\
\x0b\x41\x73\x74\x61\x6e\x61\x01\x6b\x00\x67\
\x0c\x4e\x61\x69\x72\x6f\x62\x69\x01\x2e\x00\xd4\
\x0b\x4b\x75\x77\x61\x69\x74\x01\x42\x00\x98\
\x0c\x42\x69\x73\x68\x6b\x65\x6b\x01\x71\x00\x7b\
\x0e\x56\x69\x65\x6e\x74\x69\x61\x6e\x65\x01\xa2\x00\xb0\
\x09\x52\x69\x67\x61\x01\x18\x00\x59\
\x0b\x42\x65\x69\x72\x75\x74\x01\x2c\x00\x8f\
\x0b\x4d\x61\x73\x65\x72\x75\x01\x1d\x01\x0c\
\x0d\x4d\x6f\x6e\x72\x6f\x76\x69\x61\x00\xda\x00\xc6\
\x0c\x54\x72\x69\x70\x6f\x6c\x69\x01\x04\x00\x92\
\x0a\x56\x61\x64\x75\x7a\x00\xfd\x00\x71\
\x0c\x56\x69\x6c\x6e\x69\x75\x73\x01\x1a\x00\x5e\
\x0f\x4c\x75\x78\x65\x6d\x62\x6f\x75\x72\x67\x00\xf8\x00\x6b\
\x0a\x4d\x61\x63\x61\x75\x01\xb6\x00\xa7\
\x11\x41\x6e\x74\x61\x6e\x61\x6e\x61\x72\x69\x76\x6f\x01\x41\x00\xf6\
\x0b\x53\x6b\x6f\x70\x6a\x65\x01\x13\x00\x7d\
\x0d\x4c\x69\x6c\x6f\x6e\x67\x77\x65\x01\x28\x00\xed\
\x11\x4b\x75\x61\x6c\x61\x20\x4c\x75\x6d\x70\x75\x72\x01\xa1\x00\xcc\
\x09\x4d\x61\x6c\x65\x01\x6f\x00\xca\
\x0b\x42\x61\x6d\x61\x6b\x6f\x00\xe0\x00\xba\
\x0d\x56\x61\x6c\x6c\x65\x74\x74\x61\x01\x06\x00\x8b\
\x13\x46\x6f\x72\x74\x2d\x64\x65\x2d\x46\x72\x61\x6e\x63\x65\x00\x81\x00\xb6\
\x0f\x4e\x6f\x75\x61\x6b\x63\x68\x6f\x74\x74\x01\x53\x00\xf9\
\x0e\x4d\x61\x6d\x6f\x75\x64\x7a\x6f\x75\x01\x3d\x00\xea\
\x0b\x4d\x65\x78\x69\x63\x6f\x00\x3d\x00\xad\
\x0d\x43\x68\x69\x73\x69\x6e\x61\x75\x01\x20\x00\x71\
\x0b\x4d\x61\x70\x75\x74\x6f\x01\x26\x01\x04\
\x0b\x59\x61\x6e\x67\x6f\x6e\x01\x97\x00\xb2\
\x0d\x57\x69\x6e\x64\x68\x6f\x65\x6b\x01\x0b\x00\xfe\
\x0e\x4b\x61\x74\x68\x6d\x61\x6e\x64\x75\x01\x84\x00\x9c\
\x0e\x41\x6d\x73\x74\x65\x72\x64\x61\x6d\x00\xf5\x00\x64\
\x0f\x57\x69\x6c\x6c\x65\x6d\x73\x74\x61\x64\x00\x73\x00\xbb\
\x0c\x4d\x61\x6e\x61\x67\x75\x61\x00\x54\x00\xbb\
\x0b\x4e\x69\x61\x6d\x65\x79\x00\xf1\x00\xb9\
\x0a\x41\x62\x75\x6a\x61\x00\xfa\x00\xc1\
\x0e\x50\x79\x6f\x6e\x67\x79\x61\x6e\x67\x01\xcb\x00\x83\
\x0b\x53\x61\x69\x70\x61\x6e\x01\xef\x00\xb5\
\x09\x4f\x73\x6c\x6f\x01\x00\x00\x50\
\x0b\x4d\x61\x73\x71\x61\x74\x01\x54\x00\xa5\
\x0e\x49\x73\x6c\x61\x6d\x61\x62\x61\x64\x01\x6f\x00\x90\
\x0a\x4b\x6f\x72\x6f\x72\x01\xdb\x00\xc4\
\x0b\x50\x61\x6e\x61\x6d\x61\x00\x61\x00\xc1\
\x11\x50\x6f\x72\x74\x20\x4d\x6f\x72\x65\x73\x62\x79\x01\xf2\x00\xe4\
\x0d\x41\x73\x75\x6e\x63\x69\x6f\x6e\x00\x87\x01\x03\
\x09\x4c\x69\x6d\x61\x00\x65\x00\xe9\
\x0b\x4d\x61\x6e\x69\x6c\x61\x01\xc3\x00\xb6\
\x0b\x57\x61\x72\x73\x61\x77\x01\x12\x00\x64\
\x0b\x4c\x69\x73\x62\x6f\x6e\x00\xdd\x00\x85\
\x0d\x53\x61\x6e\x20\x4a\x75\x61\x6e\x00\x78\x00\xaf\
\x09\x44\x6f\x68\x61\x01\x48\x00\xa1\
\x0a\x53\x65\x6f\x75\x6c\x01\xcd\x00\x87\
\x0e\x42\x75\x63\x75\x72\x65\x73\x74\x69\x01\x1b\x00\x77\
\x0b\x4d\x6f\x73\x6b\x76\x61\x01\x2f\x00\x5b\
\x0b\x4b\x69\x67\x61\x6c\x69\x01\x22\x00\xd5\
\x0f\x42\x61\x73\x73\x65\x74\x65\x72\x72\x65\x00\x7e\x00\xb1\
\x0d\x43\x61\x73\x74\x72\x69\x65\x73\x00\x82\x00\xb7\
\x11\x53\x61\x69\x6e\x74\x2d\x50\x69\x65\x72\x72\x65\x00\x8a\x00\x72\
\x0e\x4b\x69\x6e\x67\x73\x74\x6f\x77\x6e\x00\x81\x00\xb9\
\x0f\x53\x61\x6e\x20\x4d\x61\x72\x69\x6e\x6f\x01\x03\x00\x79\
\x0d\x53\x61\x6f\x20\x54\x6f\x6d\x65\x00\xf8\x00\xd2\
\x0b\x52\x69\x79\x61\x64\x68\x01\x3f\x00\xa2\
\x0a\x44\x61\x6b\x61\x72\x00\xce\x00\xb6\
\x0d\x46\x72\x65\x65\x74\x6f\x77\x6e\x00\xd6\x00\xc2\
\x0f\x42\x72\x61\x74\x69\x73\x6c\x61\x76\x61\x01\x0b\x00\x6e\
\x0e\x4c\x6a\x75\x62\x6c\x6a\x61\x6e\x61\x01\x06\x00\x73\
\x0e\x4d\x6f\x67\x61\x64\x69\x73\x68\x75\x01\x3d\x00\xce\
\x0e\x43\x61\x70\x65\x20\x54\x6f\x77\x6e\x01\x1f\x01\x04\
\x0b\x4d\x61\x64\x72\x69\x64\x00\xe7\x00\x81\
\x0d\x4b\x68\x61\x72\x74\x6f\x75\x6d\x01\x26\x00\xb5\
\x0f\x50\x61\x72\x61\x6d\x61\x72\x69\x62\x6f\x00\x8b\x00\xc8\
\x0c\x4d\x62\x61\x62\x61\x6e\x65\x01\x24\x01\x05\
\x0e\x53\x74\x6f\x63\x6b\x68\x6f\x6c\x6d\x01\x0d\x00\x51\
\x09\x42\x65\x72\x6e\x00\xfa\x00\x72\
\x0d\x44\x61\x6d\x61\x73\x63\x75\x73\x01\x2d\x00\x90\
\x0d\x44\x75\x73\x68\x61\x6e\x62\x65\x01\x66\x00\x85\
\x0c\x42\x61\x6e\x67\x6b\x6f\x6b\x01\x9f\x00\xb8\
\x09\x4c\x6f\x6d\x65\x00\xef\x00\xc6\
\x0a\x54\x75\x6e\x69\x73\x00\xff\x00\x89\
\x0b\x41\x6e\x6b\x61\x72\x61\x01\x27\x00\x82\
\x0d\x41\x73\x68\x67\x61\x62\x61\x74\x01\x53\x00\x86\
\x0c\x4b\x61\x6d\x70\x61\x6c\x61\x01\x26\x00\xd2\
\x12\x4b\x69\x65\x76\x20\x28\x52\x75\x73\x73\x69\x61\x29\x01\x23\x00\x69\
\x0e\x41\x62\x75\x20\x44\x68\x61\x62\x69\x01\x4d\x00\xa3\
\x0b\x4c\x6f\x6e\x64\x6f\x6e\x00\xed\x00\x66\
\x0b\x44\x6f\x64\x6f\x6d\x61\x01\x2c\x00\xde\
\x12\x57\x61\x73\x68\x69\x6e\x67\x74\x6f\x6e\x20\x44\x43\x00\x65\x00\x81\
\x15\x43\x68\x61\x72\x6c\x6f\x74\x74\x65\x20\x41\x6d\x61\x6c\x69\x65\x00\x7b\x00\xaf\
\x0f\x4d\x6f\x6e\x74\x65\x76\x69\x64\x65\x6f\x00\x8a\x01\x17\
\x0d\x54\x61\x73\x68\x6b\x65\x6e\x74\x01\x67\x00\x7f\
\x0c\x43\x61\x72\x61\x63\x61\x73\x00\x77\x00\xbe\
\x0a\x48\x61\x6e\x6f\x69\x01\xa8\x00\xa9\
\x0d\x42\x65\x6c\x67\x72\x61\x64\x65\x01\x11\x00\x77\
\x0b\x4c\x75\x73\x61\x6b\x61\x01\x1f\x00\xf0\
\x0b\x48\x61\x72\x61\x72\x65\x01\x24\x00\xf4\
'