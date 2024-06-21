import streamlit as st
import pandas as pd
import plotly.express as px
import math
from matplotlib import pyplot as plt
from math import log
# from tkinter.filedialog import asksaveasfilename
# from tkinter.filedialog import askopenfilename

import csv

# from csv import DictReader

# Session State
# "st.session_state :", st.session_state


# st.write("### Page 1")
st.markdown("<h1 style='text-align: center;'>Pipe heat loss calculation </h1>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<h3 style='text-align: Left;'>Input data </h3>", unsafe_allow_html=True)
st.markdown('---')

# Leggi file con diametri e genera lista diametri
diaList = []
with open('files/diametri.csv', newline='') as diameters:
    diameters_data = csv.reader(diameters)
    next(diameters_data) #salta la riga di testa

    for row in diameters_data:
        diaList.append(row[0])
        #print(diaList)

with open('files/Dia_thk.csv') as file_thk:
    df = pd.read_csv(file_thk, delimiter = ";")   # lettura file e creazione dataFrame

# file_thk = open('files/Dia_thk.csv')
# df = pd.read_csv(file_thk, delimiter = ";")   # lettura file e creazione dataFrame
# df.columns   # Read Headers

# form1 = st.form("Data Form", clear_on_submit= True, border= True)

with open('files/ExtDia.csv') as file_extDia:
    dfDia = pd.read_csv(file_extDia, delimiter = ";", index_col= 1)   # lettura file e creazione dataFrame e indicizzazione secondo colonna 1 (DN)


def diaSelected():
    
    return

def thkSelected():

    return

# with st.form("Data Form", clear_on_submit=True, border=True):
col1, col2 = st.columns(2)
    # extDia = col1.slider(":blue[Pipe nominal diameter (inches)]", min_value=0, max_value=100)
    # thk = col2.number_input(":blue[Pipe thickness (mm)]")
    # myList = ["1/8", "opt2", "opt3"]
option_dia = col1.selectbox ("Select Diameter [inches]", options=(diaList), on_change= diaSelected, key="DN")

thkList = df[option_dia].dropna()
option_thk = col2.selectbox("Select Thickness [mm]", options=(thkList), on_change= thkSelected, key= "thksel")
externalDia = dfDia.loc[option_dia, 'Dia']
# thk = float(option_thk)
# intDia = extDia-2*thk
thk = float(option_thk.replace(",","."))
extDia = float(externalDia.replace(",","."))
intDia = extDia-2*thk


st.session_state['extDia']= extDia
st.session_state['thk'] = thk
st.session_state['intDia']= intDia


# st.session_state

print(type(option_thk))
print("option_thk =", option_thk)
print("Thk =", thk)
print("intDia =", intDia)


# col1.markdown("<br>", unsafe_allow_html=True)
# col1.markdown("<h3 style='text-align: left;'> Thermal data </h3>", unsafe_allow_html=True) # Dati termici
# col2.markdown("<br>", unsafe_allow_html=True)
# col2.markdown("<h3><br></h3>", unsafe_allow_html=True)
fluidTemp = col1.number_input("Fluid Temperature [°C]", value= 50, step= 1, key= 'fT')
extTemp = col2.number_input("External Temperature [°C]", value= 20, step= 1, key= 'eT')
flowRate = col1.number_input("Fluid flow rate [kg/h]", value = 50.1, step= 0.1, key= 'fR')
specHeat = col2.number_input("Specific heat [kcal/kg°C]", value=0.500, step= 0.005, format="%0.3f", key= 'sH')

condPipe = col1.number_input("Lambda Pipe [W/m°K]", value= 52, key= 'cP' )   # valore tipico acciaio
condInsul = col2.number_input("Lambda Insulation [W/m°K]", value= 0.040, step= 0.005, format="%0.3f", key= 'cI') # valore lana di roccia
hi = col1.number_input("Internal surface coeff. hi [W/m^2°K]", value= 1000, step=50, key= 'hi')
he = col2.number_input("Enternal surface coeff. he [W/m^2°K]", value= 20, step=5, key= 'he')
insulThk = col1.number_input("Insulation Thk [mm]", value= 20, step= 5, key= 'iThk')  # spessore isolante
PipeLength = col2.number_input("Pipe Length [m]", value = 10, key= 'PLen') # lunghezza piping

# memorizza dati di input in un dizionario -----

data= {
    "DN": [option_dia],
    "thksel": [option_thk],
    "eDia": [extDia],
    "thk": [thk],
    "iDia": [intDia],
    "fT": [fluidTemp],
    "eT": [extTemp],
    "fR": [flowRate],
    "sH": [specHeat],
    "cP": [condPipe],
    "cI": [condInsul],
    "hi": [hi],
    "he": [he],
    "iThk": [insulThk],
    "PLen": [PipeLength]
}

# -------------------------------------
dfData= pd.DataFrame(data)
print(dfData)

st.session_state

#dfDati = pd.DataFrame.from_dict((st.session_state), orient= 'index' )


#  --- calcoli -------------------------------------------
deltaT = fluidTemp-extTemp
R1 = intDia/2000 # Raggio interno in m
R2 = extDia/2000 # Raggio esterno in m
R3 = R2+insulThk/1000 # Raggio superficie isolante
L = PipeLength 
Rcrit = condInsul/he*1000 # Raggio critico
spcrit = Rcrit/1000-R2  # spessore critico

invK = (1/hi+R1/condPipe*log(R2/R1)+R1/condInsul*log(R3/R2)+R1/R3*1/he)  # 1/K inverso del coefficiente di scambio termico
Kw = 1/invK   # coeff. globale di scambio termico in W/m2°C
Kc = Kw*0.859845  # coeff di scambio in kCal/h*m2°C
Kcomb = Kc  # +Kvalvole
Qlineare = 2*math.pi*R1*Kw*deltaT   # Heat Flow in W/m
ts = Qlineare/(math.pi*((extDia+2*insulThk)/1000)*he)+extTemp   # temperatura superficie isolante

# calcolo temperatura a distanza L in m
esponente = math.pi*extDia*0.001*Kcomb/(specHeat*flowRate)
TdistL = extTemp+deltaT*math.exp(-esponente*L)   # temperatura a distanza L
Tpersa = fluidTemp-TdistL 

# dati per grafico
pitch = L/20

x=[]
Tx = []
i= 0.00
while i <= 50:
    Ti = extTemp+deltaT*math.exp(-i*esponente) 
    x.append(i)
    Tx.append(Ti)
    i+= pitch


# stampa risultati
st.markdown("---")

st.markdown("<h3 style='text-align: Left;'>Results </h3>", unsafe_allow_html=True)
st.markdown("---")
st.write("Selected Dia = ", option_dia, '"')
st.write("External Dia =", extDia, "mm")
st.write("Thikness =", option_thk, "mm")
st.write("Internal Dia =", intDia, "mm")
st.write("DT =", deltaT, "°C")
st.write("")
Testo = "Temperature @ distance of " + str(L) + " m ="
st.write(Testo, TdistL, "°C")
st.write("Lost Temperature =", Tpersa, "°C")
st.write("<br><br>", unsafe_allow_html=True)


#fig = plt.plot(x, Tx)
#plt.show()
# st.pyplot(fig)
# print("x, Tx", x, Tx)
# fig= px.line(data_frame= [x, Tx], x= "distanza", y= "Temperatura")

# Rappresentazione grafica perdita di temperatura
dfg = pd.DataFrame({'dist (m)': x, 'T (°C)': Tx})
chart_data = pd.DataFrame({'dist (m)': x, 'Temp (°C)': Tx})
st.line_chart(
   chart_data, x= "dist (m)", y= "Temp (°C)", color=["#FF0000"]  # Optional
)

dfg_ni= st.dataframe(dfg, hide_index=True)    # tabella numerica
# st.write(dfg_ni)

print("Q/L e ts", Qlineare, ts)
print("TdistL, Tlost", TdistL, Tpersa)

st.markdown("---")
   
# btnCalc = st.form_submit_button("run")
col1, col2, col3, col4 = st.columns(4)

btn1 = col1.button("Go to Page 2", disabled=False)
btnSave = col2.button("Save data", disabled= False)
btnLoad = col3.button("Load data", disabled= False)

sceltaDatiFile = st.sidebar.radio("Dati da File", ["1", "2"])

if btn1:
    st.write("button clicked!")
    for i in range(1000):
        aaa  = i+1
    st.switch_page("pages/page_2.py")

if btnSave:
    st.write("button Save clicked!")
    #nuovofile = 'nuovoFile.csv'
    # datafile = st.file_uploader("Upload CSV",type=['csv'])

    # fileName = asksaveasfilename(defaultextension= 'csv')
    #st.write(fileName)
    #with open(fileName, 'w') as f:
    #if datafile is not None:
    #    file_details = {"FileName":datafile.name,"FileType":datafile.type}
        # df  = pd.read_csv(datafile)      
        #dfData
    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode("utf-8")

    daticsv = convert_df(dfData)
    
    st.download_button(
        label= "Download data as csv",
        data= daticsv,
        file_name= "dataInput.csv",
        mime= "text/csv"
        )
        
        # f.write(dfDia)
     #   save_uploadedfile(datafile)

if sceltaDatiFile == "1":
    st.write("button Load clicked!")
    st.subheader("Dataset")
    # archivio = st.file_uploader("Load a data file")
    # datafile = st.file_uploader("Upload CSV",type=['csv'])
    #  st.success("Saved File")
    #nomeArchivio = askopenfilename(defaultextension= 'csv')
    datafile = st.file_uploader("upload file dati", type= ['csv'])
    
    print("datafile =", datafile)
    
    if datafile is not None:
        file_details = {"FileName": datafile.name, "File Type": datafile.type}
        # file_details = {"FileName": datafile.name, "File Type": datafile.type}
        #with open(nomeArchivio) as f:
        #      dati = pd.read_csv(f, delimiter = "," )   # lettura file e creazione dataFrame
        
        dati = pd.read_csv(datafile)
        st.dataframe(dati)
        for i in range(10000):
            i+=1
        DN = dati.loc[0, 'DN'] 
        thksel = dati.loc[0,'thksel']
        eDia = dati.loc[0,'eDia']
        thk = dati.loc[0,'thk']
        iDia = dati.loc[0,'iDia']
        fT = dati.loc[0,'fT']

        st.write("DN = ", DN)
    
        # Delete all the items in Session state
        for key in st.session_state.keys():
            del st.session_state[key]
        
        st.session_state['DN']= str(DN)
        st.session_state['thksel']= str(thksel) 
        st.session_state['extDia']= eDia
        st.session_state['thk']= thk
        st.session_state['iDia']= iDia
        st.session_state['fT']= fT




       
        # st.switch_page("pages/page_1.py")
    
    
    

