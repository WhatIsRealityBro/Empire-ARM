from __future__ import print_function
from builtins import str
from builtins import object
from lib.common import helpers

class Module(object):

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'Find-DomainProcess',

            'Author': ['@harmj0y'],

            'Description': ('Query the process lists of remote machines, searching for processes with a specific name or owned by a specific user. Part of PowerView.'),

            'Software': 'S0194',

            'Techniques': ['T1057'],

            'Background' : True,

            'OutputExtension' : None,
            
            'NeedsAdmin' : False,

            'OpsecSafe' : True,
            
            'Language' : 'powershell',

            'MinLanguageVersion' : '2',
            
            'Comments': [
                'https://github.com/PowerShellMafia/PowerSploit/blob/dev/Recon/'
            ]
        }

        # any options needed by the module, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Agent' : {
                'Description'   :   'Agent to run module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'ComputerName' : {
                'Description'   :   'Hosts to enumerate.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ComputerDomain' : {
                'Description'   :   'Specifies the domain to query for computers, defaults to the current domain.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ComputerLDAPFilter' : {
                'Description'   :   'Host filter name to query AD for, wildcards accepted.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ComputerSearchBase' : {
                'Description'   :   'Specifies the LDAP source to search through for computers',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ComputerUnconstrained' : {
                'Description'   :   'Switch. Search computer objects that have unconstrained delegation.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ComputerOperatingSystem' : {
                'Description'   :   'Return computers with a specific operating system, wildcards accepted.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ComputerServicePack' : {
                'Description'   :   'Return computers with the specified service pack, wildcards accepted.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ComputerSiteName' : {
                'Description'   :   'Return computers in the specific AD Site name, wildcards accepted.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ProcessName' : {
                'Description'   :   'The name of the process to hunt, or a comma separated list of names.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'UserGroupIdentity' : {
                'Description'   :   'Specifies a group identity to query for target users, defaults to "Domain Admins".',
                'Required'      :   False,
                'Value'         :   ''
            },
            'UserAdminCount' : {
                'Description'   :   'Switch. Search for users with "(adminCount=1)" (meaning are/were privileged)',
                'Required'      :   False,
                'Value'         :   ''
            },
            'UserIdentity' : {
                'Description'   :   'Specifies one or more user identities to search for.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'UserLDAPFilter' : {
                'Description'   :   'A customized ldap filter string to use for user enumeration, e.g. "(description=*admin*)"',
                'Required'      :   False,
                'Value'         :   ''
            },
            'UserSearchBase' : {
                'Description'   :   'Specifies the LDAP source to search through for target users.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'StopOnSuccess' : {
                'Description'   :   'Switch. Stop hunting after finding after finding a target user.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Delay' : {
                'Description'   :   'Delay between enumerating hosts, defaults to 0.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Domain' : {
                'Description'   :   'The domain to use for the query, defaults to the current domain.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Server' : {
                'Description'   :   'Specifies an active directory server (domain controller) to bind to',
                'Required'      :   False,
                'Value'         :   ''
            },
            'SearchScope' : {
                'Description'   :   'Specifies the scope to search under, Base/OneLevel/Subtree (default of Subtree)',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ResultPageSize' : {
                'Description'   :   'Specifies the PageSize to set for the LDAP searcher object.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ServerTimeLimit' : {
                'Description'   :   'Specifies the maximum amount of time the server spends searching. Default of 120 seconds.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Tombstone' : {
                'Description'   :   'Switch. Specifies that the search should also return deleted/tombstoned objects.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Jitter' : {
                'Description'   :   'Specifies the jitter (0-1.0) to apply to any specified -Delay, defaults to +/- 0.3.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Threads' : {
                'Description'   :   'The maximum concurrent threads to execute.',
                'Required'      :   False,
                'Value'         :   ''
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu

        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value


    def generate(self, obfuscate=False, obfuscationCommand=""):
        
        moduleName = self.info["Name"]
        
        # read in the common powerview.ps1 module source code
        moduleSource = self.mainMenu.installPath + "/data/module_source/situational_awareness/network/powerview.ps1"

        try:
            f = open(moduleSource, 'r')
        except:
            print(helpers.color("[!] Could not read module source path at: " + str(moduleSource)))
            return ""

        moduleCode = f.read()
        f.close()

        # get just the code needed for the specified function
        script = helpers.strip_powershell_comments(moduleCode)

        script += "\n" + moduleName + " "

        for option,values in self.options.items():
            if option.lower() != "agent":
                if values['Value'] and values['Value'] != '':
                    if values['Value'].lower() == "true":
                        # if we're just adding a switch
                        script += " -" + str(option)
                    else:
                        script += " -" + str(option) + " " + str(values['Value']) 

        script += ' | Out-String | %{$_ + \"`n\"};"`n'+str(moduleName)+' completed!"'
        if obfuscate:
            script = helpers.obfuscate(self.mainMenu.installPath, psScript=script, obfuscationCommand=obfuscationCommand)
        return script
