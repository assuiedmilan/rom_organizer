XML_DOCUMENT = """<?xml version="1.0"?>
<gameList>
    <provider>
        <System>psx</System>
        <software>Skraper</software>
        <database>ScreenScraper.fr</database>
        <web>http://www.screenscraper.fr</web>
    </provider>
    <game id="19562" source="ScreenScraper.fr">
        <path>./Akuji the Heartless.pbp</path>
        <name>Akuji The Heartless</name>
        <desc>The premise of Akuji the Heartless is not a happy one. Just as Akuji, a voodoo shaman, was about to get married, his bride-to-be was kidnapped and he was then killed by his very own brother. His seemingly loving sibling then ripped out his heart and sent Akuji to a dark and evil underworld. Akuji swore revenge on his brother and promised to avenge his true love.     As Akuji, you must collect the souls of your departed ancestors and give them to Baron Samedi, watcher of the underworld. If you are successful, he will grant your wish of revenge by giving you the opportunity to face your brother and do unto him as he did to you. More importantly, you will be together with your fiancee once again.    </desc>
        <rating>0.7</rating>
        <releasedate>19980624T000000</releasedate>
        <developer>Crystal Dynamics</developer>
        <publisher>Eidos Interactive</publisher>
        <genre>Platform-Action / Adventure-Action</genre>
        <players>1</players>
        <image>./media/images/Akuji the Heartless.png</image>
        <thumbnail>./media/box3d/Akuji the Heartless.png</thumbnail>
    </game>
    <game id="19369" source="ScreenScraper.fr">
		<path>./Alundra 2 - A New Legend Begins.pbp</path>
		<name>Alundra 2 : A New Legend Begins</name>
		<desc>Alundra 2: The Mystery of Machinevolution is an action/puzzle video game developed by Contrail and published by Activision. It was released in Japan in 1999 and in North America and Europe in the next year. Unlike its predecessor, Alundra, Alundra 2 features a new 3D look which opens up a new world of puzzles. Because of its 3D look, rather simple plot, and the fact it has nothing to do with its predecessor apart from the name, Alundra 2 was not well received. No further Alundra titles were made, most likely because of Alundra 2's poor reception.     </desc>
		<rating>0.7</rating>
		<releasedate>20000229T000000</releasedate>
		<developer>Activision</developer>
		<publisher>Matrix Software</publisher>
		<genre>Adventure-Role playing games</genre>
		<players>1</players>
		<image>./media/images/Alundra 2 - A New Legend Begins.png</image>
		<thumbnail>./media/box3d/Alundra 2 - A New Legend Begins.png</thumbnail>
	</game>
	<game id="47072" source="ScreenScraper.fr">
		<path>./Alundra.pbp</path>
		<name>Alundra</name>
		<desc>Alundra is a boy who can step into other people's dreams. His own dreams tell him to go to the village Inoa. The ship on which Alundra is coming to the village goes down, but Alundra himself is washed up on a beach near the village. There, a blacksmith Jess takes care of him and treats him like his own son. But Alundra, stepping into the dreams of the village people, understands there's a danger somewhere. The people have horrible nightmares, and only Alundra can find out what they mean...    Alundra is an action role playing game (RPG) somewhat similar to the famous Zelda games. It uses real-time combat and has a lot of physical and environmental puzzles. A big part of the game is spent in dungeons, where the player has to solve puzzles in order to proceed.</desc>
		<rating>0.9</rating>
		<releasedate>19971231T000000</releasedate>
		<developer>Sony</developer>
		<publisher>Psygnosis</publisher>
		<genre>RolePlayingGames</genre>
		<players>1</players>
		<image>./media/images/Alundra.png</image>
		<thumbnail>./media/box3d/Alundra.png</thumbnail>
		<favorite>true</favorite>
	</game>
	<game id="19493" source="ScreenScraper.fr">
		<path>./Ape Escape.pbp</path>
		<name>Ape Escape</name>
		<desc>A boisterous band of baboons carry out a daring zoo escape. It's ape anarchy and it's up to you to stop the chimps before they make chumps out of the human race! Use both analog sticks to operate great gadgets including a Tank, a Remote Control Car, a Stun Club, and a Time Net in your quest to hunt down over 200 apes!</desc>
		<rating>0.75</rating>
		<releasedate>19990531T000000</releasedate>
		<developer>Sony</developer>
		<publisher>Sony</publisher>
		<genre>Platform-----Action</genre>
		<players>1</players>
		<image>./media/images/Ape Escape.png</image>
		<thumbnail>./media/box3d/Ape Escape.png</thumbnail>
	</game>
</gameList>
"""

GENRE = 'genre'
NAME = 'name'
PATH = 'path'
FILE = "filename"

EXPECTED_DATA = [
    {NAME: 'Akuji The Heartless', GENRE: 'Platform-Action-Adventure-Action', FILE: 'Akuji the Heartless.pbp'},
    {NAME: 'Alundra 2 : A New Legend Begins', GENRE: 'Adventure-Role-playing-games', FILE: 'Alundra 2 - A New Legend Begins.pbp'},
    {NAME: 'Alundra', GENRE: 'RolePlayingGames', FILE: 'Alundra.pbp'},
    {NAME: 'Ape Escape', GENRE: 'Platform-Action', FILE: 'Ape Escape.pbp'},
]

expected_names = [game.get(NAME) for game in EXPECTED_DATA]
expected_genres = [game.get(GENRE) for game in EXPECTED_DATA]
expected_paths = ['./' + game.get(FILE) for game in EXPECTED_DATA]
expected_files = [game.get(FILE) for game in EXPECTED_DATA]