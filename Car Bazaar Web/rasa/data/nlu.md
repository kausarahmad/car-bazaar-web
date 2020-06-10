## lookup:make
data/lookup_tables/make.txt

## lookup:model
data/lookup_tables/model.txt

## lookup:body_type
data/lookup_tables/body_type.txt

## lookup:fuel_type
data/lookup_tables/fuel_type.txt

## lookup:badge
data/lookup_tables/badge.txt

## lookup:city
data/lookup_tables/city.txt

## intent:greet
- hey
- hello
- hi
- good morning
- good evening
- hey there
- whaddup
- what's up
- wassup
- hiya
- hello you
- hi there
- hey u
- helo u
- henlo
- salam
- howdy
- hihi
- sup
- yo
- yooooooo
- aoa
- assalamoalaikum

## intent:goodbye
- bye
- bi
- bi bi
- bubye
- goodbye
- see you around
- see you later
- see ya
- c ya
- cya
- ciao
- ok bye
- catch ya later
- catch u later
- catch you later
- khuda hafiz
- night night
- allah hafiz
- shab bakhair
- goodnight

## intent:affirm
- yes
- indeed
- yep
- yup
- yeah
- sounds cool
- cool
- ok cool
- that's right
- great
- of course
- that sounds good
- correct
- okay
- ok

## intent:deny
- no
- never
- I don't think so
- don't like that
- nope
- nonono
- i'm not satisfied
- this isn't right
- this is not right
- does not look right
- i dont like this
- nah man
- nahhh
- no way
- not really

## intent:change_make
- change the brand to [hyundai](make)
- change the car to [nissan](make)
- i want to find out about [subaru](make)
- let's look at a [rover](make) instead
- tell me about [ford](make) instead
- change the make back to [subaru](make)
- change the car company to a [smart](make)
- change the brand to [mercedes](make:Mercedes-Benz)
- tell me about [Mercedes-Benz](make)
- change the make of my car to [mclaren](make)
- change the make of the car to [mazda](make)

## intent:change_model
- change the model to [patrol](model)
- change the model to [pathfinder](model)
- change model to [x-trail](model)
- change the model to [x trail](model)
- change the model to [range](model)
- change model to [grange](model)
- change model to [super pursuit](model)
- lets change the model to [xtrail](model)
- show me a nissan [altima](model)
- change the car model to [GLE500](model)
- change the car model to [370gt](model)
- please change the car model to [tiida](model)
- i want to find out about the [Mercedes](make:Mercedes-Benz) [sls](model)
- tell me about the [Double six](model) model
- tell me about the [daimler](make) [double six](model) model
- change the model to [520S](model)
- change the model to [720s](model)
- show me a mclaren [650s](model)
- change the model to [mp4 12c](model)
- change the model of the mclaren to [MP4-12c](model)
- change model to [10/20](model)
- change the car model to [senna](model)
- i want to find out about the [mclaren](make) [675lt](model)

## intent:change_badge
- can I see the same car in [GLI](badge) ?
- change the specs to [xe](badge)
- change the specification to [xl](badge)
- change the badge to [ti-4x4](badge)
- change the badge to [Ti 4x4](badge)
- show me this car in a [st 4x4](badge)
- change the specs to [2WD](badge)
- change the specs to [stl](badge)
- change the badge to [st 4x4](badge)
- change badge to [STX](badge)
- change spec to [ST 4wd](badge)
- update the specs to [st-4x4](badge)
- let's change the specification of the car to [Raptor](badge)
- change the badge to [xline](badge)
- same model with [xline](badge) specification
- show me this car in the [gli] badge
- change the specs of the car to [313 CDI MWB](badge)
- change the spec to [313 cdi mwb](badge)
- can you tell me the price of the same car but a [Luxury](badge)
- i want to set the badge to [90-TSI-Comfortline](badge)
- change the specification to [ASCENT SPORT](badge)
- yes change the badge to [sport red](badge)

## intent:change_city
- show me this car in [castle hill](city)
- what would this car cost in [adelaide](city)
- change the city to [queens park](city)
- change the location to [Canberra](city)
- can you show me the same car in [Kensington](city)
- what would this car cost in [melbourne](city)
- change the city to [Hammond Park](city)
- change the location to [North Sydney](city)
- show me this car in [sydney](city)
- show me the same car in [yallambie](city)
- is this car cheaper in [Croom](city)
- what is the price of this car in [rosebery](city)
- can I buy this car in [Richmond](city)
- change the city to [northampton](city)
- change the location to [Canberra](city)
- show me this car in [Kensington](city)
- what would this car cost in [granville](city)
- can you change the location to [southport](city)
- change the location to [port melbourne](city)

## intent:change_body_type
- change the body type to [SUV](body_type)
- show me an [suv](body_type)
- tell me the price of a [sedan](body_type) of the same car
- yes change body to a [hatchback](body_type)
- show me this car in a [wagon](body_type)
- change the body style of my car to a [Hatch](body_type)
- I want to see a [coupe](body_type)
- change it to [Ute](body_type)
- show me the price of a [minivan](body_type:Van/Minivan)
- change the car to an [automatic](body_type)
- change the body type to a [convertible](body_type)

## intent:change_fuel_type
- change the car to [petrol](fuel_type)
- change fuel to [gas](fuel_type)
- change fuel type to [diesel](fuel_type)

## intent:change_year
- Show me the same car with [2001](year) model
- Change the year to [2015](year)
- What was the price of car with [2013](year) model
- Lets see the same car with model of year [2019](year)
- How much does this car cost with [2018](year) model
- how much does a [1998](year) model of this car cost?
- change the year of the car to [1970](year)
- change car year to [1800](year)

## intent:change_mileage
- Show me the same car with mileage more than [3000](mileage) km
- Show me the same car with mileage less than [1000](mileage)km
- Change the mileage to [0](mileage) km
- Lets increase the mileage to [60000](mileage) km
- Lets decrease the mileage of the car to [287318](mileage) km
- What if we change the mileage to [46700](mileage) km

## intent:ask_cheap_city
- in which city would this car be cheaper?
- from where can I buy this car cheapest?
- which city would sell a low cost car?
- where would this car be lowest cost?
- if I want a cheap car with these specifications, which city should I buy in?
- which city has the most economical rates for this car?
- in what location would I find this car for cheaper?
- which locations sell this car for less?
- where can I get a cheap version of this car from?
- where is this car cheaper?
- where is this model cheap?

## intent:ask_badge_list
- can I know what other specs this car comes in?
- what other specifications does this car come in?
- what badges does this car have?
- show me all badges of this car
- i want to find out about the other specs of this car
- tell me about other badges of this car
- tell me about other specifications of this car

## intent:ask_body_list
- what body types does this car come in?
- list body styles this car comes in
- list all other bodies of this car

## intent:ask_model_list
- can you show me all the models of this car?
- what other models does this brand have?
- what models does this car have
- are there other models of this brand I can buy?
- show me more models of the same make
- show me models of this brand
- show me the models of this company
- list the models of this car

## intent:ask_fuel_list
- what fuel types does this car come in?
- what other fuel types does this car run on
- can you list the fuels this car runs on?
- list the fuels
- list fuel types this car has

## intent:ask_cheap_badge
- Price with different badges?
- which specs are cheaper?
- list the cheapest specifications this car comes in
- tell me the low cost specification this car has
- which badges of this car are cheaper?
- which specs are cheaper in this model?
- which specifications cost less?
- tell me the price with different car specifications

## intent:bot_challenge
- are you a bot?
- are you a human?
- am I talking to a bot?
- am I talking to a human?
- who are you?

## intent:save
- please save my conversation
- can I donwload my conversation?
- can I keep this conversation?
- save this conversation for me
- save it
- save this conversation
- please save my convo thanks

## intent:scream
- aaaaaaaaa
- aaaa
- AAAAAAAAAA
- AAAAAAAAAAAAAA
- aaaaaaaaaaaaaaaAAAAAAAAAAAAAA

## intent:ask_price
- What's the price of this car?
- Tell me its price
- tell me the price of this car
- what is the price of my car
- how much is my car costing me right now
- how much does this car cost
- how much do i need to spend on this car
- how much can i sell this car for