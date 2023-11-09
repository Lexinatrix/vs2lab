import splitter as sp
import mapper as ma
import reducer as re

splitter = sp.Splitter()
#print("created Splitter")
mappers = {
    ma.Mapper(),
    ma.Mapper(),
    ma.Mapper()
}
#print("created Mappers")
reducers = {
    re.Reducer("5558"),
    re.Reducer("5559")
}
#print("created Reducers")

#put text into splitter
text = "ABC XYZ FEG\nGHJ LKS UET\nPOS GUT QZC\nABC XYZ FEG\nGHJ LKS UET\nPOS GUT QZC\nABC XYZ FEG\nGHJ LKS UET\nPOS GUT QZC\n"
splitter.putText(text)

splitter.start()
#print("started splitter")

for mapper in mappers:
    mapper.start()

#print("started mappers")

for reducer in reducers:
    reducer.start()

#print("started reducers")