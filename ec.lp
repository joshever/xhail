%% E. Examples
#example holdsAt(available(lactose), 1).
#example holdsAt(available(lactose), 2).
#example not holdsAt(available(lactose), 3).

%% M. Modes
#modeh happens(apply($sugar),+time) :3~5.
#modeb holdsAt($fluent,+time).
#modeb not holdsAt($fluent,+time).
