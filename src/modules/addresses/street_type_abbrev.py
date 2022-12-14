STREET_TYPES = {
    # https://www.stylemanual.gov.au/grammar-punctuation-and-conventions/names-and-terms/australian-place-names
    # https://meteor.aihw.gov.au/content/270020
    # https://meteor.aihw.gov.au/content/429840
    # https://api-doc.cacheinvest.com.au/street_type_guideline.html
    'Accs': 'Access',
    'Ally': 'Alley',
    'Alwy': 'Alleyway',
    'Ambl': 'Amble',
    'App': 'Approach',
    'Arc': 'Arcade',
    'Artl': 'Arterial',
    'Ancg': 'Anchorage',
    'Arty': 'Artery',
    'Art': 'Artery',
    'Ave': 'Avenue',
    'Ba': 'Banan',
    'Basn': 'Basin',
    'Bend': 'Bend',
    'Bch': 'Beach',
    'Blk': 'Block',
    'Bwlk': 'Boardwalk',
    'Bvd': 'Boulevard',
    'Blvd': 'Boulevard',
    'Br': 'Brace',
    'Brae': 'Brae',
    'Brk': 'Break',
    'Bdge': 'Bridge',
    'Brow': 'Brow',
    'Bdwy': 'Broadway',
    'Bypa': 'Bypass',
    'Bywy': 'Byway',
    'Cswy': 'Causeway',
    'Ctr': 'Centre',
    'Ch': 'Chase',
    'Cir': 'Circle',
    'Clt': 'Circlet',
    'Cct': 'Circuit',
    'Crcs': 'Circus',
    'Cl': 'Close',
    'Clde': 'Colonnade',
    'Cmmn': 'Common',
    'Con': 'Concourse',
    'Cps': 'Copse',
    'Crn': 'Corner',
    'Cso': 'Corso',
    'Ct': 'Court',
    'Crt': 'Court',
    'Ctyd': 'Courtyard',
    'Cove': 'Cove',
    'Cres': 'Crescent',
    'Crst': 'Crest',
    'Crss': 'Cross',
    'Crsg': 'Crossing',
    'Crd': 'Crossroad',
    'Cowy': 'Crossway',
    'Cuwy': 'Cruiseway',
    'Cds': 'Cul-de-sac',
    'Cutt': 'Cutting',
    'Dale': 'Dale',
    'Dell': 'Dell',
    'Devn': 'Deviation',
    'Dip': 'Dip',
    'Dstr': 'Distributor',
    'Dr': 'Drive',
    'Dve': 'Drive',
    'Dvwy': 'Driveway',
    'Edge': 'Edge',
    'Elb': 'Elbow',
    'End': 'End',
    'Ent': 'Entrance',
    'Esp': 'Esplanade',
    'Est': 'Estate',
    'Extn': 'Extension',
    'Exp': 'Expressway',
    'Fawy': 'Fairway',
    'Ftrk': 'Fire',
    'Fitr': 'Firetrail',
    'Flat': 'Flat',
    'Folw': 'Follow',
    'Ftwy': 'Footway',
    'Fshr': 'Foreshore',
    'Form': 'Formation',
    'Fwy': 'Freeway',
    'Frnt': 'Front',
    'Frtg': 'Frontage',
    'Gap': 'Gap',
    'Gdn': 'Garden',
    'Gdns': 'Gardens',
    'Gte': 'Gate',
    'Glde': 'Glade',
    'Glen': 'Glen',
    'Gra': 'Grange',
    'Grn': 'Green',
    'Grnd': 'Ground',
    'Gr': 'Grove',
    'Gly': 'Gully',
    'Hts': 'Heights',
    'Hird': 'Highroad',
    'Hwy': 'Highway',
    'Hill': 'Hill',
    'Intg': 'Interchange',
    'Intn': 'Intersection',
    'Jnc': 'Junction',
    'Key': 'Key',
    'Ldg': 'Landing',
    'Lane': 'Lane',
    'Lnwy': 'Laneway',
    'Lees': 'Lees',
    'Line': 'Line',
    'Link': 'Link',
    'Lt': 'Little',
    'Lkt': 'Lookout',
    'Loop': 'Loop',
    'Lwr': 'Lower',
    'Mall': 'Mall',
    'Mndr': 'Meander',
    'Mew': 'Mew',
    'Mews': 'Mews',
    'Mtwy': 'Motorway',
    'Nook': 'Nook',
    'Otlk': 'Outlook',
    'Pde': 'Parade',
    'Park': 'Park',
    'Pkld': 'Parklands',
    'Pwy': 'Parkway',
    'Part': 'Part',
    'Pass': 'Pass',
    'Psge': 'Passage',
    'Path': 'Path',
    'Pway': 'Pathway',
    'Piaz': 'Piazza',
    'Plza': 'Plaza',
    'Pkt': 'Pocket',
    'Pnt': 'Point',
    'Port': 'Port',
    'Prom': 'Promenade',
    'Pl': 'Place',
    'Plat': 'Plateau',
    'Qdrt': 'Quadrant',
    'Quad': 'Quad',
    'Qdgl': 'Quadrangle',
    'Qy': 'Quay',
    'Qys': 'Quays',
    'Rmbl': 'Ramble',
    'Ramp': 'Ramp',
    'Rnge': 'Range',
    'Rch': 'Reach',
    'Rest': 'Rest',
    'Res': 'Reserve',
    'Rtt': 'Retreat',
    'Ride': 'Ride',
    'Rdge': 'Ridge',
    'Rgwy': 'Ridgeway',
    'Rise': 'Rise',
    'Rvr': 'River',
    'Rvwy': 'Riverway',
    'Rvra': 'Riviera',
    'Rowy': 'Right',
    'Ring': 'Ring',
    'Rd': 'Road',
    'Rds': 'Roads',
    'Rdsd': 'Roadside',
    'Rdwy': 'Roadway',
    'Rnde': 'Ronde',
    'Rty': 'Rotary',
    'Rsbl': 'Rosebowl',
    'Rte': 'Route',
    'Rty': 'Rotary',
    'Row': 'Row',
    'Rnd': 'Round',
    'Rte': 'Route',
    'Rue': 'Rue',
    'Run': 'Run',
    'Swy': 'Service',
    'Svwy': 'Serviceway',
    'Sdng': 'Siding',
    'Slpe': 'Slope',
    'Snd': 'Sound',
    'Shun': 'Shunt',
    'Spur': 'Spur',
    'Sq': 'Square',
    'Strs': 'Stairs',
    'Shwy': 'State',
    'Stps': 'Steps',
    'Stra': 'Strand',
    'St': 'Street',
    'Strp': 'Strip',
    'Sbwy': 'Subway',
    'Tarn': 'Tarn',
    'Tce': 'Terrace',
    'Thfr': 'Thoroughfare',
    'Tlwy': 'Tollway',
    'Top': 'Top',
    'Tor': 'Tor',
    'Twrs': 'Towers',
    'Trk': 'Track',
    'Trl': 'Trail',
    'Trlr': 'Trailer',
    'Tri': 'Triangle',
    'Tkwy': 'Trunkway',
    'Turn': 'Turn',
    'Upas': 'Underpass',
    'Upr': 'Upper',
    'Vale': 'Vale',
    'Viad': 'Viaduct',
    'View': 'View',
    'Vlls': 'Villas',
    'Vsta': 'Vista',
    'Wade': 'Wade',
    'Walk': 'Walk',
    'Wkwy': 'Walkway',
    'Wy': 'Way',
    'Whrf': 'Wharf',
    'Wynd': 'Wynd',
    'Yard': 'Yard',
}
