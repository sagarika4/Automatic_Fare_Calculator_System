import numpy as np
import time
class FareCalculator:
    def __init__(self, img_path,database,license_plate):
        self.img = img_path  
        self.df = database  
        self.licplate=license_plate
    def insert_df(self,vehicle_type):
       self.df.loc[len(self.df)]=[self.licplate,vehicle_type,time.time()]
       return self.df
    
        
    def check_existence(self):
        return (self.df['License_Plate_Number']==self.licplate).any()
    def calculate_fare(self):
        exit_time=time.time()
        entry_time=self.df.loc[self.df['License_Plate_Number']==self.licplate,'Entry Time'].iloc[0]
        duration=(exit_time-entry_time)/60
        vehicle_type=self.df.loc[self.df['License_Plate_Number']==self.licplate,'Vehicle Type'].iloc[0]
        if vehicle_type=='Car':
            fare=20
            if (duration-60)>0:
                fare+=(duration-60)*0.4
        else:
            fare=10
            if(duration-60)>0:
                fare+=(duration-60)*0.2
        return fare
    def remove_entry(self):
        self.df=self.df[self.df.License_Plate_Number != self.licplate]
        return self.df
