import re

def get_social_fingerprint_influenced( bloc_str, dimension='action_content_syntactic' ):
    #https://www.nature.com/articles/s41598-022-11854-w
    '''
        A - plain text
        T - plain mention
        G - plain retweet
        C - tweet with media/URLs
    '''

    if( dimension == 'action_content_syntactic' ):
        #replace all non "Tr(mMEU)" characters
        sfi = re.sub(r'[^Tr(mMEU)]', '', bloc_str)
        sfi = sfi.replace('()', '')

        #remove - duplicate E's and m's - start
        sfi = re.sub(r'[U]', 'E', sfi)#urls map to media

        sfi = sfi.replace('(E', '(Ǝ')
        sfi = sfi.replace('(m', '(ɯ')
        sfi = sfi.replace('(M', '(ɯ')

        sfi = re.sub(r'[mE]', '', sfi)
        #remove - duplicate E's and m's - end

        sfi = re.sub(r'[T]', 'A', sfi) #tweet 
        sfi = re.sub(r'\(ɯ\)', 'T', sfi) #mention 
        sfi = re.sub(r'[r]', 'G', sfi) #retweet
        sfi = re.sub(r'\(Ǝ\)', 'C', sfi) #media/URL 
        return [{ 'text': sfi, 'type': 'sf_influenced' }]
    
    return []
    

def get_social_fingerprint_frm_bloc( bloc_str, dimension='action' ):

    #social fingerprint based on: https://ieeexplore.ieee.org/abstract/document/7876716    

    def bloc_sf_content_map(bloc_str, typ):

        sf = ''
        bloc_str = bloc_str.strip()
        if( bloc_str == '' ):
            return ''
        
        if( typ == 'b3_content' ):
            if( bloc_str == 't' ):
                sf = 'N' #N: tweet contains no entities (plaintext)
            elif( len(set(bloc_str)) == 1 ):
                sf = 'E' #E: tweet contains entities of one type
            else:
                sf = 'X' #X: tweet contains entities of mixed types

            return sf
        

        bloc_sf_b6_content_map = {
            't': 'N', #N: tweet contains no entities (plaintext)
            'U': 'U', #U: tweet contains 1+ URLs
            'H': 'H', #H: tweet contains 1+ Hashtags
            'm': 'M', #M: tweet contains 1+ Mentions
            'M': 'M', #M: tweet contains 1+ Mentions
            'E': 'D'  #D: tweet contains 1+ Media
        }
        
        ori = bloc_str
        bloc_str = ''.join( set(bloc_str) )
        if( len(bloc_str) > 1 ):
            sf = 'X'
        else:
            sf = bloc_sf_b6_content_map.get(bloc_str, '')
        
        return sf
    
    if( dimension == 'action' ):
        sf = re.sub(r'[^Tpr]', '', bloc_str)
        sf = re.sub(r'[T]', 'A', sf) #tweet 
        sf = re.sub(r'[p]', 'C', sf) #reply
        sf = re.sub(r'[r]', 'T', sf) #retweet
        return [{ 'text': sf, 'type': 'b3_type' }]

    elif( dimension == 'content_syntactic' ):
        sf = re.sub(r'[ (|*]', '', bloc_str)
        sf = sf.split(')')
        sf = [ s for s in sf if s != '' ]
        
        b3_c = [ bloc_sf_content_map(s, 'b3_content') for s in sf ]
        b6_c = [ bloc_sf_content_map(s, 'b6_content') for s in sf ]
        
        return [
            {'text': ''.join(b3_c), 'type': 'b3_content'},
            {'text': ''.join(b6_c), 'type': 'b6_content'}
        ]
    
    return []