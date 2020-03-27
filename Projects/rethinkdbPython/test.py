from rethinkdb import r
r.connect('172.17.0.2', 28015).repl()
#r.db_create('python_tutorial').run()
#r.db('python_tutorial').table_create('heroes').run()
heroes = r.db('python_tutorial').table('heroes')
"""heroes.insert({
    "hero": "Wolverine",
    "name": "James 'Logan' Howlett",
    "magazine_titles": ["Amazing Spider-Man vs. Wolverine", "Avengers",
        "X-MEN Unlimited", "Magneto War", "Prime"],
    "appearances_count": 98
}).run()"""
"""heroes.insert([
    {
        "hero": "Magneto", 
        "name": "Max Eisenhardt", 
        "aka": ["Magnus", "Erik Lehnsherr", "Lehnsherr"],  
        "magazine_titles": ["Alpha Flight", "Avengers", "Avengers West Coast"],
        "appearances_count": 42
    },
    {   
        "hero": "Professor Xavier", 
        "name": "Charles Francis Xavier", 
        "magazine_titles": ["Alpha Flight", "Avengers", "Bishop", "Defenders"],
        "appearances_count": 72
    },
    {
        "hero": "Storm", 
        "name": "Ororo Monroe", 
        "magazine_titles": ["Amazing Spider-Man vs. Wolverine", "Excalibur",
            "Fantastic Four", "Iron Fist"],
        "appearances_count": 72
    }
]).run()"""
heroes.run()
r.table(heroes)