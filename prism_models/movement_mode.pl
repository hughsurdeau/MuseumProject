mdp

// probabilities that channels change status
// channel of user 1
const double p1 = 0.8; // probability channel remains on
const double r1 = 0.2; // probability channel moves from off to on 



module room
//State of the room should represent the likilihood of overall norm
//Takes as input: flows into lobby, flows out to galls 1 & 2
//Ratio of wanderers to walkers
//Ratio of # of people 

	// Result state (prevalence of wandering ratios)
	// 0 = init, 1 = Wanderers prevail 2 = Linear prevail
	r : [0..2] init 0;
	// Local state (surpluss ratio of people compared to expected)
	s : [0..5] init 4;
	// wanderer ratio. 5 = all wanderers
	w : [0..5] init 4;

	// Transition functions
	// Transition should focus around linear impact 
	// Wanderer ratio
	[] w=5 -> (r'=1);
	[] w=0 -> (r'=2);


	// w=1 transitions
	[] s=0 & w = 1 -> 0.5 : (w'=0) + 0.35 : (w'=1) + 0.15 : (w'=2);
	[] s=1 & w = 1 -> 0.35 : (w'=0) + 0.5 : (w'=1) + 0.15 : (w'=2);
	[] s=2 & w = 1 -> 0.15 : (w'=0) + 0.35 : (w'=1) + 0.5 : (w'=2);
	[] s=3 & w = 1 -> 0.10 : (w'=0) + 0.30 : (w'=1) + 0.6 : (w'=2);
	[] s=4 & w = 1 -> 0.05 : (w'=0) + 0.25 : (w'=1) + 0.7 : (w'=2);
	[] s=5 & w = 1 -> 0.2 : (w'=1) + 0.8 : (w'=2);

	
	// w=2 transitions
	[] s=0 & w = 2 -> 0.6 : (w'=1) + 0.30 : (w'=2) + 0.10 : (w'=3);
	[] s=1 & w = 2 -> 0.5 : (w'=1) + 0.35 : (w'=2) + 0.15 : (w'=3);
	[] s=2 & w = 2 -> 0.35 : (w'=1) + 0.5 : (w'=2) + 0.15 : (w'=3);
	[] s=3 & w = 2 -> 0.15 : (w'=1) + 0.35 : (w'=2) + 0.5 : (w'=3);
	[] s=4 & w = 2 -> 0.10 : (w'=1) + 0.30 : (w'=2) + 0.6 : (w'=3);
	[] s=5 & w = 2 -> 0.05 : (w'=1) + 0.25 : (w'=2) + 0.7 : (w'=3);


	// w=3 transitions
	[] s=0 & w = 3 -> 0.7 : (w'=2) + 0.25 : (w'=3) + 0.05 : (w'=4);
	[] s=1 & w = 3 -> 0.6 : (w'=2) + 0.30 : (w'=3) + 0.10 : (w'=4);
	[] s=2 & w = 3 -> 0.5 : (w'=2) + 0.35 : (w'=3) + 0.15 : (w'=4);
	[] s=3 & w = 3 -> 0.35 : (w'=2) + 0.5 : (w'=3) + 0.15 : (w'=4);
	[] s=4 & w = 3 -> 0.15 : (w'=2) + 0.35 : (w'=3) + 0.5 : (w'=4);
	[] s=5 & w = 3 -> 0.05 : (w'=2) + 0.25 : (w'=3) + 0.7 : (w'=4);


	// w=4 transitions
	[] s=0 & w = 4 -> 0.8 : (w'=3) + 0.2 : (w'=4);
	[] s=1 & w = 4 -> 0.7 : (w'=3) + 0.25 : (w'=4) + 0.05 : (w'=5);
	[] s=2 & w = 4 -> 0.6 : (w'=3) + 0.30 : (w'=4) + 0.10 : (w'=5);
	[] s=3 & w = 4 -> 0.5 : (w'=3) + 0.35 : (w'=4) + 0.15 : (w'=5);
	[] s=4 & w = 4 -> 0.35 : (w'=3) + 0.5 : (w'=4) + 0.15 : (w'=5);
	[] s=5 & w = 4 -> 0.15 : (w'=3) + 0.35 : (w'=4) + 0.5 : (w'=5);

endmodule

