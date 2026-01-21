# Evaluating Police Responses to Emergencies
## How quickly are police respondingto 911 calls in Seattle?
## Data & Programming for Public Policy (Fall 2024) Mitchell Bobbin & Neil Stein
The research question was borne out of a common trope in American culture: Call the police and then order a pizza from a nearby shop and expect the pizza to get there first
We are set about to test the veracity of this perception with Python, using data from the Vera Institute of Justice and Seattle Business license data. We further explore the relationship between demographics observed at the Census tract level to evaluate this relationsip.
Our goal with this research is to explore the variability in police response times, the relative distribution of police & pizza restaurants, and to plot out key insights from this exploration.
We began by filtering the 5 million rows of data to just 911 calls to capture police responding to calls that are urgent, reducing the data to approximately 2 million entries. We then cleaned the data, calculated response times for each individual call, and classified each call by its initial description when the dispatcher received the call.

## Results
Our city-wide analysis found that the average response time for a 911 call was over 42 minutes, and is higher than a 2023 study (insert link here) found the expected delivery time for a pizza of around 30 minutes.
There's significant variation among the different police beats within the dataset as well. Concerningly, the B1, B2, and B3 precincts are well above the average city-wide time by almost 20 minutes: a 50% longer response time.
<img width="1829" height="562" alt="image" src="https://github.com/user-attachments/assets/92c5a86c-da0a-477c-b541-0a04ed3ce9f8" />

Further, we examined the difference among the different call types to examine whether police were responding with the expected urgency an emergency requires. The results seem to track the relative urgency overall: Police respond much quicker to violent crime calls than any other with the noise complaint being the least urgent of them all. It is worth noting that before categorizing the calls that a large number were described vaguely as "disturbance", obfuscating any specificity that could point to a more serious situation like a domestic violence scenario. Ultimately, these were classified as noise complaints due to limited information.
<img width="937" height="959" alt="image" src="https://github.com/user-attachments/assets/6620c2c9-cfc1-4667-a53a-5f1aa1b541d5" />

Next, we examined how police responses varied based upon the demographics of where the call was originating. Since Seattle is a whiter than average city, we deemed a census tract as more diverse on average than the rest of the city or whiter than average to the rest of the city to explore how race may also play a role within these categories.

<img width="1100" height="800" alt="image" src="https://github.com/user-attachments/assets/6bd495c6-16cf-47d4-99ba-8bc4f5e3691a" />

We found that whiter than average census tracts had slower than average police response times across all call types, and much slower than the response time for the same type of calls compared to more diverse neighborhoods. We postulate that there is probably some overpolicing happening in these more diverse neighbhorhoods to explain this disparity.

We further built a shiny app to allow a user to explore the variation among response times with regard to where in the city the call originates, and compare it to the average response time in that neighborhood generally.
<img width="1100" height="500" alt="image" src="https://github.com/user-attachments/assets/0d3a6791-b96c-4009-a7ab-10a830702ef2" />

We then look to explore the distribution of pizza restarants throughout the city, and police stations which can give one an idea of how the dispatching of these officers may be limited geographically. The distribution of pizza restaurants heavily favors northern parts of Seattle, away from the demographically diverse southern part of the city
Police station distributions are clustered in the center of the city, near UW and financial district. There's fewer stations in industrial and lower-income neighborhoods

<img width="937" height="959" alt="image" src="https://github.com/user-attachments/assets/7bc76850-2540-430c-96ea-26d856a31d7d" />

## Policy Questions and Implications
What are the costs of adding police stations?
Do dispatchers need more training to gather more meaningful information that can communicate call urgency?
What are the costs of increasing police presence in communities with slow response times?
Are police inundated with too many 911 calls? Can educating the public help divert calls to other channels in non emergency situations?

## Opportunities for Further Research

Has response time improved over the span of the data?
How significantly do initial call and final disposition vary?
How many ‘near misses’ occurred, i.e. where the call ended up being life-or-death but the initial disposition made it seem more trivial?
Would increased accountability on 911 dispatchers impact response times?
Are there significant differences in response times when officers leave from the station vs. answer the call while on patrol?


