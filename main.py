#import cast_upgrade_1_5_21  #@UnusedImport
import os
import time
from cast.application import ApplicationLevelExtension
import logging
import subprocess
from cast.application import publish_report
from cast.application import create_postgres_engine
import subprocess, sys
import zipfile
import glob
import re
import csv
from cast.application.managment import AnalysisUnit


class FindMissingSource(ApplicationLevelExtension):
    def __init__(self):
        pass
    
    def start_application(self, application):
        """
        Called before analysis.
        
        .. versionadded:: CAIP 8.3
        
        :type application: :class:`cast.application.Application`
        @type application: cast.application.Application
        """
        pass    

  
    def end_application(self, application):
        class_path = 'C:/'   
        #ks = application.get_knowledge_base()
        kb= application.get_managment_base()
        app_name= kb.get_applications()
        logging.info("App process started..." + str(app_name))
       
        indexx = 1
        Log_fileName = ''
        deploy_pathName = ''
        java_list = []
        class_final = []
        final_list_values = []
        for deploy_path in kb.execute_query("""(select deploypath from cms_pref_sources)"""):                
            if deploy_path[0]:
                deploy_pathName =  deploy_path[0]
                logging.info("Deploy Path --- " + str(deploy_pathName))
            else:
                logging.info("deploy_path Condition false") 
        for source_path in kb.execute_query("""(select deploypath from cms_portf_application)"""):                
            if source_path[0]:
                source_pathName =  source_path[0]
                logging.info("Source Path   " + str(source_pathName))
            
            else:
                logging.info("source_path  Condition false") 
        for line in kb.execute_query("""(select distinct(execlog) from cms_j2ee_analysis)"""):
            
            if line[0]:
                Log_fileName =  line[0]                     
                logging.info("Line zero value --- " + str(Log_fileName))
                
            else:
                logging.info("Condition false") 
        find_filepath = self.get_plugin().directory
        logging.info("find_filepath   " +str(find_filepath)) 
        find_missingSource(self,application,Log_fileName, deploy_pathName,find_filepath)
        
        os.chdir(find_filepath)
        logging.info("Changed dir--->  "+ str(os.getcwd()))
        for file in glob.glob("missingSource.csv"):
            logging.info("File found..." + file)
            csv_fileName = file
            java_list = reading_csv(self,application,csv_fileName)
           #logging.info("Java List in csv..." + str(java_list[12]))
        #find_missingSource(self,application,Log_fileName,deploy_pathName)
        class_final = find_jar_classes(source_pathName)   
        logging.info("file for Jars-->  " + str(class_final[0]))
        final_list_values = [i for i in class_final + java_list if i not in class_final]
        logging.info("final_list_values    " + str(final_list_values[0])) 
        for working_path in kb.execute_query("""(select workingpath from cms_pref_sources)"""):       
            working_pathName =  working_path[0] 
            dmt_data_dir = os.path.join(working_pathName,'LISA')
            lisa_dir=os.path.join(self.dmt_data_dir,self.lisapath.replace('-',''))
            logging.info("LISA Dir..   "+str(lisa_dir))
        write_csv(self,lisa_dir,app_name,final_list_values)
        logging.info("CSV Generated")

def find_missingSource(self, application,log_fileName,deploy_pathName,find_filepath):      
        
        """
        Called after module content creation.
        Gives you the central's application.
        
        .. versionadded:: CAIP 8.3
        
        :type application: :class:`cast.application.central.Application`        
        @type application: cast.application.central.Application
        """
   
        logging.info("Log file name passed.." + str(log_fileName))
        final_log_file = str(log_fileName).replace(' ', '@')
        logging.info("Trimed file..." + str(final_log_file))
        #logging.info("Config File Full path---> " + str(config_filepath))
        #path, filename = os.path.split(config_filepath)
        #logging.info("Config file path--> " + path + '\nConfig filename --> ' + filename + "\n")
        
        powershell_filepath = os.path.realpath("powershell.exe")
        #logging.info("Config File Full path---> " + str(powershell_filepath))
        pwpath, pwfilename = os.path.split(powershell_filepath)
        #logging.info("Config file path--> " + pwpath + '\nConfig filename --> ' + pwfilename + "\n")
        powerShellPath='C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe'
        #powerShellCmd='C:\SDK\com.custsoftware.findMissingSource\FindMissingSources.ps1'
        #os.chdir(deploy_pathName)
        os.chdir(find_filepath)
        logging.info("Changed dir- find_missingSource-->  "+ str(os.getcwd()))
        arg2 = os.getcwd()
        for file in glob.glob("FindMissingSources.ps1"):
            logging.info("File found..." + file)
            ps_fileName = file
        config_filepath = os.path.realpath(ps_fileName)
        logging.info("config_filepath..   " + str(config_filepath))
        #cwd=os.getcwd()
        #logging.info("Env value-----" + str(cwd))
        #logging.info("Log file path----------" + str(log_fileName)) 
        
        #p = subprocess.Popen([r'C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe', 
         #    'C:\SDK\com.custsoftware.findMissingSource\FindMissingSources.ps1'],cwd=os.getcwd())
          
        p = subprocess.Popen([r'C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe',str(config_filepath),final_log_file,str(find_filepath)])
        p.communicate()
        logging.info("Powershell executed----\n")
        
# def find_missingSource_1(self, application,log_fileName,deploy_pathName): 
#     regex = 'Cannot resolve\s*([^\n\r]*)'
#     regexsearchkey = 'Cannot resolve+\s*(\S+)\w+'
#     regexsource = '[^\s]+[a-zA-Z0-9]+\w+\.java'
#     srcpattern = 'import.*'
#     #resolve = @()
#     
#     searchkey = re.findall(regexsearchkey, open(log_fileName).read())
#     logging.info("File content matching.." + str(searchkey))
#     
#     ls = re.findall(regex, open(log_fileName).read())
#     logging.info("File content matching 22222.." + str(ls))

def reading_csv(self, application,csv_fileName):
    logging.info("CSV File---: " + str(csv_fileName))
    csv_java_list = []
    
    #file_ref = open(csv_fileName,encoding='UTF_8')   
    with open(csv_fileName,'r') as csvfile:  
        readCSV = csv.reader(csvfile)    
        row1 = []
        row2 = []
        row3 =[]
        list = []
        final_List = []
        for index,row in enumerate(readCSV):
            if index>0:
                row1.append(row[0])
                row2.append(row[1])
                row3.append(row[2])                
                for i in row2:
                    if i.endswith('.java'):
                        val = i.split('\\')
                        size = len(val)
                        java_val = val[size-1]
                        final_val = java_val.split('.')[0]
                        #logging.info("row2 size" + str(size))
                        #logging.info("Row from csv file" + str(final_val))
                        csv_java_list.append(final_val)
    #logging.info("csv_java_list-->" + str(csv_java_list))
    return csv_java_list

def write_csv(self,working_pathName,app_name,file_list):
    os.chdir(working_pathName)
    logging.info("Changed dir working_pathName--->  "+ str(os.getcwd()))
    row1 = []
    row2 = []
    row3 =[]
    list = []
    final_List = []
    file_name=os.path.join(working_pathName,'FindMissingSource_'+app_name+'.csv')
    logging.info("File Generated for missing sources..   " + str(file_name))
    for file in glob.glob("missingSource.csv"):
        #with open(file) as inf, open('out.csv','w') as outf:
        with open(file) as inf, open(file_name,'w') as outf:
            reader = csv.reader(inf,  delimiter=',')
            writer = csv.writer(outf, delimiter=',')
            writer.writerow(["Missing Source Path","Package Name"])
            for index,row in enumerate(reader):
                if index>0:
                    if row[1].strip() is None or row[1].strip() == '':
                         #logging.info("values from file.."+ str(row[1]))
                         pass
#                     if (row[1].split("\\")).split('.')[0] in file_list:
#                         logging.info("Found")
#                         writer.writerow(row)
                    else:
                        val_row1 = row[1].split('\\')
                        size_row1 = len(val_row1)
                        javaVal_row1 = val_row1[size_row1-1]
                        val1 = javaVal_row1.split('.')[0]
                        logging.info("val_row1.. " +str(val1))
                        row1.append(row[0])
                        row2.append(val1)
                        row3.append(row[2]) 
                                
#                     
                        l = [i for i in row2 if i in file_list]
                    #logging.info("FOUND___> " + str(l))
                        if l:
                        #logging.info("Found" + str(row[1]) +"--with--" +str(row2))
                            writer.writerow([row[1],row[2]])
                            pass
                            
def show_jar_classes(jar_file):
    list = []
    class_list =[]
    """prints out .class files from jar_file"""
    for ele in jar_file:
        #logging.info("Jar files----  " + str(ele))
        archive = zipfile.ZipFile(ele,'r')
        #list1 = archive.infolist()
        list1 = archive.namelist()
        
#         newList1 = [ele+item for item in list1]
#         list = list1 + newList1
        for zi in list1:
            fn = zi
            if fn.endswith('.class'):
                list =  os.path.basename(fn).split('.')[0]
                #logging.info ("-----Class files ------" + str(list))
                class_list.append(list)
            else:
                logging.info("No Class found Due to -No Jar present In Delivered Source Code")
                break
    return class_list
        
def find_jar_classes(source_pathName):
    
    
    changedir = os.chdir(source_pathName)
    thisdir = os.getcwd()
    logging.info("thisdir---> " + str(thisdir))
    logging.info("Changed Dir---> " + str(os.getcwd()))
    pathList1 = []
    file_lsit = []
    
    # r=root, d=directories, f = files
    for r, d, f in os.walk(thisdir):
        for file in f:
            #f = open(os.path.join(r, file), 'r')
            with open(os.path.join(r, file),'r') as f:
                if file.endswith(".jar"):
                    pathList1.append(os.path.join(r,file))
                    #logging.info("File Found---> " + str(pathList1))
                    file_lsit = show_jar_classes(pathList1)
                else:
                    logging.info("Jar not present in the delivered source code...")
                    break
    return file_lsit
                 
                