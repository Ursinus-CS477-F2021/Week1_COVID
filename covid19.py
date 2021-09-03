from vpython import *
import numpy as np

RED = vector(1, 0, 0)
MAGENTA = vector(1, 0, 1)
BLUE = vector(0, 0.5, 1)

HEALTHY = 0
INFECTED = 1
RECOVERED = 2

class Person:
    def __init__(self, res, state):
        """
        The constructor for a person

        Parameters
        ----------
        res: float
            The size of a square grid on which to have people moving
        """
        self.res = res
        # Create an initially random position
        [self.x, self.y] = (2*np.random.rand(2)-1)*res
        # Create an initial random velocity
        [self.vx, self.vy] = np.random.randn(2)*res/24
        # Create a cylinder to draw this person in vpython
        self.cylinder = cylinder(pos=vector(self.x, 0, self.y), axis=vector(0, np.sqrt(res), 0), radius=res/100, color=BLUE)
        self.state = state

    def redraw(self):
        """
        Update the drawing of this person to reflect any of
        the variables that have changed
        """
        # Update cylinder position
        self.cylinder.pos = vector(self.x, 0, self.y)
        ## Update cylinder color, as appropriate
        if self.state == HEALTHY:
            self.cylinder.color = BLUE
        elif self.state == INFECTED:
            self.cylinder.color = RED
        else:
            self.cylinder.color = MAGENTA
    
    def timestep(self, dt):
        """
        Do one step of the animation
        Parameters
        ----------
        dt: float
            Elapsed time
        """
        ## Step 1: Move person
        # Apply euler step for velocity
        self.x += dt*self.vx
        self.y += dt*self.vy
        # Check boundaries, and bounce off of them if necessary
        if np.abs(self.x) > self.res:
            self.x = np.sign(self.x)*self.res
            self.vx *= -1
        if np.abs(self.y) > self.res:
            self.y = np.sign(self.y)*self.res
            self.vy *= -1
        ## TODO: Keep track of how long a person has been sick

    def infect(self, other, infect_radius):
        """
        Parameters
        ----------
        other: Person
            A person object of someone who could potentially infect self
            if other is infected and self is healthy and they are both
            close enough
        infect_radius: float
            The distance two people have to be apart in order for transmission to happen
        """
        if self.state == HEALTHY and other.state == INFECTED:
            dx = self.x - other.x
            dy = self.y - other.y
            dist = (dx**2 + dy**2)**0.5
            if dist < infect_radius:
                self.state = INFECTED

    def __str__(self):
        return "Person at ({:.3f}, {:.3f}) going {:.3f}, {:.3f}".format(self.x, self.y, self.vx, self.vy)


def do_simulation(num_people, res, infect_radius):
    """
    Parameters
    ----------
    num_people: int
        The number of people in the simulation
    res: float
        A slide length of the square grid that people are moving on
    infect_radius: float
        The distance two people have to be apart in order for transmission to happen
    """
    scene = canvas(title="Epidemic Simulation with {} People".format(num_people), width=600, height=600) 
    scene.camera.pos = vector(0, res*2, 0)
    scene.camera.axis = -scene.camera.pos
    print(scene.camera)
    people = [Person(res, INFECTED)] # First person is sick
    for i in range(num_people-1): 
        people.append(Person(res, HEALTHY)) # Everyone else is healthy
    last_time = clock()
    while True: # Animation loop
        this_time = clock()
        dt = this_time - last_time
        last_time = this_time
        for p in people:
            p.timestep(dt)
            p.redraw()

do_simulation(200, 100, 5)