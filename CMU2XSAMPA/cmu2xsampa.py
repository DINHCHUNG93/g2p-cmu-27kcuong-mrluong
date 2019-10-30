import re
import codecs
def ParseFileToDict(file, assert2fields = False, value_processor = None):
     if value_processor is None:
         value_processor = lambda x: x[0]
     dict = {}
     for line in codecs.open(file,'r','utf-8-sig'):
         parts = line.split()
         if assert2fields:
            assert(len(parts) == 2)
         dict[parts[0]] = value_processor(parts[1:])
     return dict

def ParseFileToList(file):
    list=[]
    with codecs.open(file,'r','utf-8-sig') as inf:
         for line in inf:
            list.append(line.strip())
    return list

cmudict=ParseFileToList('data/cmudict-0.7b.arpabet')
a2x_vowels=ParseFileToDict('data/ARPABET2XSAMPA-vowels', value_processor = lambda x: " ".join(x))
a2x_vowels_keys=sorted(a2x_vowels.keys())
a2x_consonants=ParseFileToDict('data/ARPABET2XSAMPA-consonants-Bac', value_processor = lambda x: " ".join(x))
a2x_consonants_key=sorted(a2x_consonants.keys())
#cmu_xsam_tone=open('cmudict-0.7b.xsampa.tone','w')
cmu_xsam=open('cmudict-0.7b.vi-xsampa','w')
for line in cmudict:    
    line=re.sub(' +',' ',line.strip())
    iterms=line.split()
    word=iterms[0]
    #phones=' '.join(iterms[1:])
    isvowel=0
    outt=""
    out=""
    for phone in iterms[1:]:
        phone=re.sub('[0-9]','',phone)        
        if phone in a2x_vowels_keys: # is a vowel     
            if len(a2x_vowels[phone].split())>1:       
                out = out + ' ' + a2x_vowels[phone].split()[0] + '_1' + ' ' + a2x_vowels[phone].split()[1]
            else:
                out = out + ' ' + a2x_vowels[phone] + '_1'
        elif phone in a2x_consonants_key:
            out = out + ' ' + a2x_consonants[phone]
        else:
            print("ERROR: " + line)
            continue
    cmu_xsam.write(word.strip().lower() + ' ' + out.strip() + '\n')
cmu_xsam.close()


