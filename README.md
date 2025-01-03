# GIK2NX_Assignment02

1. Designing an application using Kivy, KivyMD
2. Web scraping data like temperature, humidity, pressure and visibility using at least two websites (E.g., “timeanddate.com”, “wunderground.com”)
3. Handling errors to avoid crashing of application
4. Storing extracted data using Firebase, local DB (like Microsoft Access, MySQL, PostgreSQL, etc) and another alternate location like text file (Replication)
5. Your reflection on the tasks

# To do list:
- Bryt ut "fetch_firebase/SQLite/txt etc till egna funktioner.
- Fixa så att inte txtfilen dubbellagrar?
- Eventuellt adda converters för Farenheit --> Celsius + inHG --> mBar + miles --> km (för att kringgå wunderbaums amerikanska SHIT)
- Snygga till UI (kivy), lägga till grid exempelvis
- Eventuell funktionalitet för om ett värde (exempelvis visibility) inte går att nås från en webbplats, hämta från backup webbplatsen istället (om timeanddate inte funkar, hämta från wunderbaum)

# Done:
- Se till så att alla typer av lagring kan nås om det behövs, se till så alla backups fungerar för att undvika errors och krascher
- Felmedelanden CHECK
- Kolla över när man söker på hela landet istället för endast landskoden i wunderground [/weather/sweden/kumla] ist för [/weather/se/sater], description saknas då och temperature blir "--" CHECK! 
- Funktionalitet för att göra om ländernas namn till country codes om det inte går att hitta CHECK!
- Fixa med datesen (SQLite & Firebase) THOMAS TROR DET ÄR FIXAT! :)
- Fixa Så att inte multipla lagringar sker (samma stad och land lagras flera ggr i firebase, SQLite & txt [där är det okej att samma stad/loand lagras flera ggr, men inte med samma datum]) CHECK!