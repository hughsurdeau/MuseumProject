mdp

// probabilities that channels change status
// channel of user 1
const double p1 = 0.8; // probability channel remains on
const double r1 = 0.2; // probability channel moves from off to on


const int expectedPeoplePerRoom = 10; // Expected number of people per room


module room
//State of the room should represent the likilihood of overall norm
//Takes as input: flows into lobby, flows out to galls 1 & 2
//Ratio of wanderers to walkers
//Ratio of # of people 

	// Result state (prevalence of wandering ratios)
	r : [0..9] init 0;
	// Local state (surpluss ratio of people 
	s : [0..5] init 2;

endmodule