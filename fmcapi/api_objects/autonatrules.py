from .apiclasstemplate import APIClassTemplate
from .ftdnatpolicy import FTDNatPolicy
from .ipaddresses import IPAddresses
from .interfaceobject import InterfaceObject
import logging


class AutoNatRules(APIClassTemplate):
    """
    The AutoNatRules Object in the FMC.
    """

    PREFIX_URL = '/policy/ftdnatpolicies'
    REQUIRED_FOR_POST = ["nat_id"]

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for AutoNatRules class.")
        self.parse_kwargs(**kwargs)
        self.type = "FTDAutoNatRule"

    def format_data(self):
        logging.debug("In format_data() for AutoNatRules class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'originalNetwork' in self.__dict__:
            json_data['originalNetwork'] = self.originalNetwork
        if 'translatedNetwork' in self.__dict__:
            json_data['translatedNetwork'] = self.translatedNetwork
        if 'interfaceInTranslatedNetwork' in self.__dict__:
            json_data['interfaceInTranslatedNetwork'] = self.interfaceInTranslatedNetwork
        if 'natType' in self.__dict__:
            json_data['natType'] = self.natType
        if 'interfaceIpv6' in self.__dict__:
            json_data['interfaceIpv6'] = self.interfaceIpv6
        if 'fallThrough' in self.__dict__:
            json_data['fallThrough'] = self.fallThrough
        if 'dns' in self.__dict__:
            json_data['dns'] = self.dns
        if 'routeLookup' in self.__dict__:
            json_data['routeLookup'] = self.routeLookup
        if 'noProxyArp' in self.__dict__:
            json_data['noProxyArp'] = self.noProxyArp
        if 'netToNet' in self.__dict__:
            json_data['netToNet'] = self.netToNet
        if 'sourceInterface' in self.__dict__:
            json_data['sourceInterface'] = self.sourceInterface
        if 'destinationInterface' in self.__dict__:
            json_data['destinationInterface'] = self.destinationInterface
        if 'originalPort' in self.__dict__:
            json_data['originalPort'] = self.originalPort
        if 'translatedPort' in self.__dict__:
            json_data['translatedPort'] = self.translatedPort
        if 'serviceProtocol' in self.__dict__:
            json_data['serviceProtocol'] = self.serviceProtocol
        if 'patOptions' in self.__dict__:
            json_data['patOptions'] = self.patOptions
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for AutoNatRules class.")
        if 'originalNetwork' in kwargs:
            self.originalNetwork = kwargs['originalNetwork']
        if 'translatedNetwork' in kwargs and 'interfaceInTranslatedNetwork' is True:
            logging.warning("Cannot have both a translatedNetwork and interfaceInTranslatedNetwork")
        elif 'translatedNetwork' in kwargs:
            self.translatedNetwork = kwargs['translatedNetwork']
        elif 'interfaceInTranslatedNetwork' in kwargs:
            self.interfaceInTranslatedNetwork = kwargs['interfaceInTranslatedNetwork']
        if 'natType' in kwargs:
            self.natType = kwargs['natType']
        if 'interfaceIpv6' in kwargs:
            self.interfaceIpv6 = kwargs['interfaceIpv6']
        if 'fallThrough' in kwargs:
            self.fallThrough = kwargs['fallThrough']
        if 'dns' in kwargs:
            self.dns = kwargs['dns']
        if 'routeLookup' in kwargs:
            self.routeLookup = kwargs['routeLookup']
        if 'noProxyArp' in kwargs:
            self.noProxyArp = kwargs['noProxyArp']
        if 'netToNet' in kwargs:
            self.netToNet = kwargs['netToNet']
        if 'sourceInterface' in kwargs:
            self.sourceInterface = kwargs['sourceInterface']
        if 'destinationInterface' in kwargs:
            self.destinationInterface = kwargs['destinationInterface']
        if 'originalPort' in kwargs:
            self.originalPort = kwargs['originalPort']
        if 'translatedPort' in kwargs:
            self.translatedPort = kwargs['translatedPort']
        if 'serviceProtocol' in kwargs:
            self.serviceProtocol = kwargs['serviceProtocol']
        if 'patOptions' in kwargs:
            self.patOptions = kwargs['patOptions']

    def nat_policy(self, name):
        logging.debug("In nat_policy() for AutoNatRules class.")
        ftd_nat = FTDNatPolicy(fmc=self.fmc)
        ftd_nat.get(name=name)
        if 'id' in ftd_nat.__dict__:
            self.nat_id = ftd_nat.id
            self.URL = '{}{}/{}/autonatrules'.format(self.fmc.configuration_url, self.PREFIX_URL, self.nat_id)
            self.nat_added_to_url = True
        else:
            logging.warning('FTD NAT Policy {} not found.  Cannot set up AutoNatRule for '
                            'NAT Policy.'.format(name))

    def original_network(self, name):
        logging.debug("In original_network() for AutoNatRules class.")
        ipaddresses_json = IPAddresses(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning('Network "{}" is not found in FMC.  Cannot add to originalNetwork.'.format(name))
        else:
            self.originalNetwork = new_net
            logging.info('Adding "{}" to sourceNetworks for this AutoNatRule.'.format(name))

    def translated_network(self, name):
        # Auto Nat rules can't use network group objects
        logging.debug("In translated_network() for AutoNatRules class.")
        ipaddresses_json = IPAddresses(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning('Network "{}" is not found in FMC.  Cannot add to translatedNetwork.'.format(name))
        else:
            self.translatedNetwork = new_net
            logging.info('Adding "{}" to destinationNetworks for this AutoNatRule.'.format(name))

    def source_intf(self, name):
        logging.debug("In source_intf() for AutoNatRules class.")
        intf_obj = InterfaceObject(fmc=self.fmc).get()
        items = intf_obj.get('items', [])
        new_intf = None
        for item in items:
            if item["name"] == name:
                new_intf = {'id': item['id'], 'type': item['type']}
                break
        if new_intf is None:
            logging.warning('Interface Object "{}" is not found in FMC.  Cannot add to sourceInterface.'.format(name))
        else:
            if new_intf.type == "InterfaceGroup" and len(new_intf.interfaces) > 1:
                logging.warning('Interface Object "{}" contains more than one physical interface.  '
                                'Cannot add to sourceInterface.'.format(name))
            else:
                self.sourceInterface = new_intf
                logging.info('Interface Object "{}" added to NAT Policy.'.format(name))

    def destination_intf(self, name):
        logging.debug("In destination_intf() for AutoNatRules class.")
        intf_obj = InterfaceObject(fmc=self.fmc).get()
        items = intf_obj.get('items', [])
        new_intf = None
        for item in items:
            if item["name"] == name:
                new_intf = {'id': item['id'], 'type': item['type']}
                break
        if new_intf is None:
            logging.warning('Interface Object "{}" is not found in FMC.  Cannot add to destinationInterface.'
                            .format(name))
        else:
            if new_intf.type == "InterfaceGroup" and len(new_intf.interfaces) > 1:
                logging.warning('Interface Object "{}" contains more than one physical interface.  '
                                'Cannot add to destinationInterface.'.format(name))
            else:
                self.destinationInterface = new_intf
                logging.info('Interface Object "{}" added to NAT Policy.'.format(name))

    def identity_nat(self, name):
        logging.debug("In identity_nat() for AutoNatRules class.")
        ipaddresses_json = IPAddresses(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning('Network "{}" is not found in FMC.  Cannot add to this AutoNatRule.'.format(name))
        else:
            self.natType = "STATIC"
            self.originalNetwork = new_net
            self.translatedNetwork = new_net
            logging.info('Adding "{}" to AutoNatRule.'.format(name))

    def patPool(self, name, options={}):
        # Network Group Object permitted for patPool
        ipaddresses_json = IPAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroup(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', []) + networkgroup_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'name': item['name'], 'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning('Network "{}" is not found in FMC.  Cannot add to patPool.'.format(name))
        else:
            self.natType = "DYNAMIC"
            self.patOptions = {"patPoolAddress": new_net}
            self.patOptions["interfacePat"] = options.interfacePat if "interfacePat" in options.keys() else False
            self.patOptions["includeReserve"] = options.includeReserve if "includeReserve" in options.keys() else False
            self.patOptions["roundRobin"] = options.roundRobin if "roundRobin" in options.keys() else True
            self.patOptions["extendedPat"] = options.extendedPat if "extendedPat" in options.keys() else False
            self.patOptions["flatPortRange"] = options.flatPortRange if "flatPortRange" in options.keys() else False
            logging.info('Adding "{}" to patPool for this AutoNatRule.'.format(name))