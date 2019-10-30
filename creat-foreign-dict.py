import sys
import codecs
import re
vi_ref_dict="resources/all-vietnamese-syllables_17k9.XSAMPA.3Mien.BAC-HUE-NAM_endingsound.lex"
cuong_27k="resources/27k-Cuong.lex"
cmu_xsampa="CMU2XSAMPA/cmudict-0.7b.vi-xsampa"
manual_dict="resources/oov_manual"
## parse a file intro dictionary
def ParseFileToDict(file, assert2fields = False, value_processor = None):
    if value_processor is None:
        value_processor = lambda x: x[0]
    dict = {}
    for line in codecs.open(file,'r','utf-8-sig'):
        parts = line.split()
        if assert2fields:
            assert(len(parts) == 2)
        if parts[0] not in dict.keys():
            dict[parts[0]] = value_processor(parts[1:])
    return dict
#################
all_Vei_lex=ParseFileToDict(vi_ref_dict, value_processor = lambda x: " ".join(x))
all_Vei_lex_keys=sorted(all_Vei_lex.keys())
cuong_lex=ParseFileToDict(cuong_27k, value_processor = lambda x: " ".join(x))
cuong_lex_keys=sorted(cuong_lex.keys())
cmu_lex=ParseFileToDict(cmu_xsampa, value_processor = lambda x: " ".join(x))
cmu_lex_keys=sorted(cmu_lex.keys())
manual_lex=ParseFileToDict(manual_dict, value_processor = lambda x: " ".join(x))
#################
# Get lexion for a specific dialect
def get_Vie_lex_mien(dictlex,word,mien='B'):
    all_dict_keys = sorted(dictlex.keys())
    output=''
    if word in all_dict_keys: # found a lexixon for this word            
                lexs=dictlex[word].split('=')
                lexs.remove('')
                if len(lexs)==3:
                    if mien=='B':
                        output=lexs[0]
                    elif mien=='C':
                        output=lexs[1]
                    elif mien=='N':
                        output=lexs[2]
    return output
# Creating a lexicion for foreign words
# this function buid lexicon from a file that contains lines in which each line in a formart as:
# word1 word2 ? vi-syllable1  vi-syllable2 ...
# Note: Diterminer '?' must be '\t' in text file input
def convert_foreign(fileforeign):
    ## Reference Vie-Lex         
    dictout = {}
    with codecs.open(fileforeign,'r','utf-8-sig') as inf:
        for line in inf:
            line=line.strip()            
            line=line.lower()
            iterms=line.split('\t')
            if len(iterms)==2:
                words=iterms[0].split()                
                pronuciations=iterms[1].split()
                if len(words)==len(pronuciations) or len(words)==1:
                    if len(words)==1:
                        pronuciations='_'.join(pronuciations).split()
                    possition=0
                    for word in words: # for each syllable in words
                        possition=possition+1                        
                        if word not in dictout.keys():
                            cac_mien=['B','C','N']
                            tmp_phones=''
                            for mien in cac_mien:                    
                                if mien=='B': # BAC
                                    key=word
                                elif mien=='C': # HUE
                                    key=word + '(HUE)'
                                elif mien=='N': # NAM
                                    key=word + '(NAM)'
                                error=0
                                phonemes=''                                
                                a_tmp=pronuciations[possition-1].split('_')                                
                                for syl in a_tmp:                                    
                                    lex_mien_out= get_Vie_lex_mien(all_Vei_lex,syl,mien)                                    
                                    if lex_mien_out=='':
                                        error=1
                                        break
                                    else:
                                        phonemes = phonemes + ' ' + re.sub(' ','|',lex_mien_out.strip())
                                        #phonemes = phonemes + ' ' + lex_mien_out.strip()
                                if error==0:
                                    phonemes=re.sub(' +',' ',phonemes).strip()
                                    if phonemes!=tmp_phones:
                                        dictout[key]=phonemes
                                        tmp_phones=phonemes
                else:
                    print('ERROR missing pronunciation: ' + line)
            else:
                print('ERROR bad line: ' + line)    
    return dictout
    
### MAIN
infile=sys.argv[1] # input file in mr-Luong fortmat
outlex=convert_foreign(infile)
#print('Searching in Cuong27k Lexicion')
### Looking for lex in Cuong-27k that is not in MrLuong-lex to write to output file
#for key in cuong_lex_keys:
#    if key not in outlex:
#        if key.isalpha():
#            outlex[key]=cuong_lex[key]     
print('Searching in CMU Lexicion Lexicion')   
### Looking for lex in CMU-lex that is not in MrLuong-lex to write to output file
for key in cmu_lex_keys:
    if key.isalpha():
        if key not in outlex:
            outlex[key]=re.sub(' ','|',cmu_lex[key].strip())      
print("Writing to file")  
write_foreign=codecs.open('foreign-MrLuong-And-Cuong-And-CMU.lex','w','utf-8')
### Appending the manual lexicion to the output
manual_lex_keys=sorted(manual_lex.keys())
for key in manual_lex_keys:
    if key not in outlex:
        outlex[key]=manual_lex[key]
### Writing MrLuong-lex to output file
outlex_keys=sorted(outlex.keys())
for key in outlex_keys:
    write_foreign.write(key + ' ' + outlex[key] + '\n')    
write_foreign.close()