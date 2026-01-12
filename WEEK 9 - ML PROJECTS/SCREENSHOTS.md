importpandasaspd fromsklearn.model\_selectionimporttrain\_test\_split

4|#LoadData

df=pd.read\_csv('../data/house\_prices.csv') df.drop('Property\_ID',axis=1,inplace=True,errors='ignore')

#One-HotEncoding df\_encoded=pd.get\_dummies(df,columns=[‘Location',‘Property\_Type'],drop\_first=True)

#Split

X=df\_encoded.drop('Price',axis=1)

13|y=df\_encoded['Price']

X\_train,X\_test,y\_train,y\_test=train\_test\_split(X,y,test\_size=0.2,random\_state=42)

#Saveprocesseddata(optionalforworkflow)\
17print('DataPrepComplete.Trainshape:',X\_train.shape)

[3]

DataPrepComplete.Trainshape:(240,8)

{}Code™MsMarkdown

03 Model Building & Evaluation

TrainingLinearRegressionandRandomForestmodels.

#%%[markdown]

##03ModelBuilding&Evaluation

#Thisnotebooktrainsthemodels.It includestheprepstepstoensurevariablesaredefined.

importpandasaspd

importnumpyasnp

fromsklearn.model\_selectionimporttrain\_test\_split fromsklearn.linear\_modelimportLinearRegression fromsklearn.ensembleimportRandomForestRegressor fromsklearn.metricsimportr2\_score,mean\_absolute\_error,mean\_squared\_error

#--- STEP1:LOAD&PREP(FixestheNameError)--- df=pd.read\_csv('../data/house\_prices.csv') if 'Property\_ID'indf.columns:

df=df.drop('Property\_ID',axis=1)

#One-HotEncoding df\_encoded=pd.get\_dummies(df,columns=['Location',‘'Property\_Type'],drop\_first=True)

#DefineXandy X=df\_encoded.drop('Price',axis=1) y=df\_encoded['Price']

#One-HotEncoding 19|df\_encoded=pd.get\_dummies(df,columns=[‘Location',‘Property\_Type'],drop\_first=True)

21|#DefineXandy

X=df\_encoded.drop('Price',axis=1) 23|y=df\_encoded['Price']

#Createthemissingvariables X\_train,X\_test,y\_train,y\_test=train\_test\_split(X,y,test\_size=0.2,random\_state=42) print("Datasuccessfullyloadedandsplit.X\_trainis nowdefined!")

#%%

#---STEP2:LINEARREGRESSION--- 31|lp\_model=LinearRegression()

LUr\_model.fit(X\_train,y\_train) 33|lp\_preds=Lr\_model.predict(X\_test)

35|print(#'LinearRegressionR2:{r2\_score(y\_test,lr\_preds):.4f}")

37|#2%

#---STEP3:RANDOMFOREST--- 39°|pf\_model=RandomForestRegressor(n\_estimators=100,random\_state=42)

rf\_model.fit(X\_train,y\_train)

rf\_preds=rf\_model.predict(X\_test)

3|print(#'RandomForestR2:{r2\_score(y\_test,rf\_preds):.4f}')

print(f'RandomForestMAE:${mean\_absolute\_error(y\_test,rf\_preds):,.2f}') [1]

Datasuccessfullyloadedandsplit.X\_trainis nowdefined! LinearRegressionR2:0.9406

RandomForestR2:0.9711

RandomForestMAE:$1,493,949.17
