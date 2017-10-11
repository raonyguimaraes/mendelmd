#import libraries
import progressbar as pb

#initialize widgets
widgets = ['Time for loop of 1 000 000 iterations: ', pb.Percentage(), ' ',  
            pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]
#initialize timer
timer = pb.ProgressBar(widgets=widgets, maxval=1000000).start()

#for loop example
for i in range(0,1000000):  
    #update
    timer.update(i)
#finish
timer.finish()  