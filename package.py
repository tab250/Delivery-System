# Package class
class Package:

    # Package Constructor
    def __init__(self, pack_list):
        self.packID = int(pack_list[0])
        self.del_address = pack_list[1]
        self.del_city = pack_list[2]
        self.del_state = pack_list[3]
        self.del_zip = pack_list[4]
        self.del_deadline = pack_list[5]
        self.pack_weight = pack_list[6]
        self.pack_note = pack_list[7]
        self.del_status = 'At hub'

    # String structure for printing Package object
    def __str__(self):
        return 'Package ID: {}, Address: {}, City/State/Zip: {}/{}/{}, ' \
               '\n Delivery Deadline: {}, Package Weight: {}, Status: {}\n'\
                .format(self.packID, self.del_address, self.del_city, self.del_state,
                        self.del_zip, self.del_deadline, self.pack_weight, self.del_status)
