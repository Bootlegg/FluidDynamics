"""
Barotropic Vorticity Equation
Holton pg 464-465
dzeta/dt = -F(x,y,t)
F(x,y,t) = d/dx...+d/dy....+beta*v_psi
Hence, we DO need a minus sign infront of cartesian beta plane term
In the end, that is, because F will get a negative sign itself, 

Overall algorithm
Initiate Zeta
1) Compute Psi from Zeta
2) Compute u,v from Psi
3) Update Zeta?
4) Repeat?


https://www.mi.uni-hamburg.de/arbeitsgruppen/theoretische-meteorologie/personen/lunkeit-frank/numerik/dokumente/barotrop.pdf
600-500hPa is pretty good for BVE, that part of the atmosphere has low divergence (BVE assumes 0 divergence)



https://apps.dtic.mil/dtic/tr/fulltext/u2/a065117.pdf
BVE can be used to model atmospheric planetary waves in the troposphere
Her har de nabla^2psi = eta-f
#Nok fordi eta-f = zeta


https://pdfs.semanticscholar.org/c937/d58642e376a098b2b319783cd121c7fbbfe9.pdf
Here,
dzeta/dt = -J(psi,nabla^2psi+f)+F+D(psi)

nabla^2 is Laplace operator
J is Jacobi operator
F is forcing function
D(psi) is diffusion term, usually -kappa*nabla^2psi (bottom-friction case)



https://www.mi.uni-hamburg.de/arbeitsgruppen/theoretische-meteorologie/personen/lunkeit-frank/numerik/dokumente/barotrop.pdf
streamfunction psi = gh/f


Rossby-Haurwitz waves, This is when,
#The STREAMFUNCTION psi, is equal to a spherical harmonic mode,
So i think this is when doing it on a sphere



#Time increment,
https://maths.ucd.ie/~plynch/eniac/CFvN-1950.pdf
Here, they talk about dt = 15min or less, something to do with gravitational waves of 300m/s
Ahh and then of course, since it's a forecast, let's say we integrate 24h forward...
so with 15 minutes, it's around 100 cycles


Domain size,
https://maths.ucd.ie/~plynch/eniac/CFvN-1950.pdf
Ahh I think understand,
they say that, if you want to forecast some area, you should actually integrate a domain slightly larger than that area
because what happens outside the domain will influence at the boundaries...
But the speed at which outside influence travels it not that great, so you only need to integrate a slightly larger domain




http://www.m-hikari.com/ams/ams-2013/ams-49-52-2013/koomsubsiriAMS49-52-2013.pdf
Here, centered differences for interior points
At top and bottom edges, they have, forward differences
and left and right edges, they have cyclic conditions

domain is X = 6000km, Y = 3000km,
d=dx=dy=93,750m
dt = 900s, integrate up to 10days,

initial vorticity:
zeta0 = 10^-4*exp(-2(k^2x^2+m^2y^2))
where 
k=2pi/(6*10^6)
m=pi/(3*10^6)

they ALSO plot the psi streamfunction! good idea, to see the gradient etc



http://empslocal.ex.ac.uk/people/staff/dbs202/cag/courses/MTMW14/notes2006.pdf
oh ok,
psi = g/f * ø
where ø is geopotential
that is the geostrophic relation?
soo... i can also calculate geopotential? ø = psi*f/g
also
zeta = dv/dx - du/dy
and since u = -dpsi/dx and v = dpsi/dy
then you get

zeta = d^2psi/dx^2 + d^2psi/dy^2
so then
nabla^2psi = zeta

you start with 500hPa geopoential ø

then btw
BCs
free-slip on north and south channel, hence v = 0 on north and south, no flow in or out of boundary
also, du/dy = 0?? no shear? on the boundaries??

this means, constant stream function on northern and southern boundary, so e.g psi = 0
and on northern and southern boundary zeta = 0

zeta = dv/dx - du/dy
zeta = 0 - 0
zeta = 0 on northern and southern boundary




solve poisson zeta = nabla^2psi
we need 2 boundary conditions, we have them, they are e.g psi = 0 on both
But I guess the problem is, it could be psi = A on northern border and psi = B on sourthen body
and apparantly we need the correct ones from the initial geopotential field 500hPa



BCs:
For bounding box, we need to set psi = 0 on ALL sides
Probably also some conditions on zeta??


https://www.mi.uni-hamburg.de/arbeitsgruppen/theoretische-meteorologie/personen/lunkeit-frank/numerik/dokumente/barotrop.pdf
#no flow across boundary, on south and northern, means v = 0
#then, you need psi constant in x direction....
#because v = dpsi/dx...
#so, along south and northern channel, i will have eg psi = 0 and v = 0
#at least... MAYBE also u = 0...
tangential, you can either have full slip, or no-slip
if no-slip, then ALSO u = 0
then, u0 = uNY+1 = 0, i'm pretty sure...
i.e the buffer zones, are equal to 0
BUT.. zeta is NOT equal to 0...
#Does this come automatically, from my jacobian atm??? or??
zeta(0,NY+1) = 2(psi(1,NY+1)-psi(0,NY))/dy^2






Robert-Asselin filters
https://www.mi.uni-hamburg.de/arbeitsgruppen/theoretische-meteorologie/personen/lunkeit-frank/numerik/dokumente/barotrop.pdf



Domains:
I should probably make buffer/ghost gridcells, +-1 on each side at least,
and as CFvN-1950 noted, you usually simulate slightly larger than what you are interested in
so both effects, grid is slightly larger than area of interest, AND we add additional cells to help with BCs





Iniital Conditions:
http://www.math.ualberta.ca/ijnam/Volume-10-2013/No-3-13/2013-03-04.pdf
Ahh, jeg tror man skal vel egentlig have initial velocity field....
faktisk
zeta = du/dy - dv/dx 
den giver jo ikke nogen unique requirement for speeds, altså, speeds på 2m/s og speeds på 400m/s,
de kan faktisk give samme relative vorticity zeta?
and btw, they set initial conditions in term of STREAM function.... they put Rossby Wave on STREAMFUNCTION
NOT as vorticity zeta?
Yeah, også Holton, Rossby-Haurwits R-H waves de er vidst defined ud fra streamfunction psi, og IKKE zeta!


Ahh ja, det er også det som Holton siger right?
Man har jo 500hPa geopotential field, og det er jo mere directly related til STREAMFUNCTION psi!



btw, det er vel som shallow water equations?
horizontal velocities er same HELE vejen op gennem atmosfære? Kinda unrealistic


barotropic_model.m from Holton, uses vorticity as initial condition, and THEN computes psi streamfunction
So I think even Holton file, probably skips some steps and doesn't QUITE follow what is more real



"""






def PsiSolvePoisson(psi,zeta,dx,dy,nx,ny):
	"""
	Solve Poisson Equation
	Holton page 465
	
	psi is streamfunction
	zeta is vorticity
	
	nabla^2psi = zeta
	
	where we are solving for psi the streamfunction, and zeta is the relative vorticity
	
	
	We set BCs at y = top and y = bottom, but not x, i think
	Following lec12.pdf here
	
	
	From lec12.pdf,
	Solving poisson equation means putting some boundary condition on psi, right?
	Because otherwise you could add any constant to psi, and it would still be able to give some curvature
	nabla^2psi = f...
	so it makes sense, to give some unique solution, we impose boundary conditions, 
	but i think, for the sake of calculating velocity, it also wouldn't matter if we added some constant to psi
	
	
	right now i'm doing psi[1:ny-1,1:nx-1]
	#So that means i'm not setting psi[bottom,x] but I AM setting psi[top,x]
	#So i think it should be psi[1:ny-2,1:nx-1]
	#Or maybe, x should also be changed...
	But, remember in Python, 1:ny-1, then 1 is included, but ny-1 is excluded, so in effect, we're doing 1:ny-2
	
	
	
	Solve Poisson Equation,
	nabla^2psi = zeta
	Elliptic PDE
	It is the steady state solution of the pseudo-time problem,
	dpsi/dt = nabla^2psi - zeta
	
	FTCS = Forward Time, Centered Space
	
	#psi1[m,n] = psi[m,n]+dt/dx^2 (psi[m-1,n]+psi[m+1,n]+psi[m,n-1]+psi[m,n+1]-4psi[m,n])-dt*zeta[m,n]
	
	#stability requires, dt <= 1/4 * dx^2
	
	Jacobi Method is choosing dt = 1/4 * dx^2
	
	

	"""
	#Compute streamfunction from vorticity
	#ζ_(i,j)^1=(((ψ_(i+1,j)-2ψ_(i,j)+ψ_(i-1,j) ))/dx^2 +((ψ_(i,j+1)-2ψ_(i,j)+ψ_(i,j-1) ))/dy^2 )

	#solve psi from lec12.pdf
	psin = np.zeros((ny,nx),dtype=np.float64)
	psin = psi.copy()
	
	
	#I should, imo, be explicit and set BCs psi = 0....
	
	##JACOBI METHOD
	#dtau = 0.5*0.5*(0.5*dx**2+0.5*dy**2)
	for r in range(500): #pseudo-time
	
	
		#We should probably do a copy, because, otherwise, we are doing intermediate changes...
		#i.e we are changing values that will be used later, that shouldn't....
		#So, that is, to really follow the algorithm, we need to copy the values...
		#At least, most likely... if it was a double for loop, then we would have to....
		#BUT, MAYBE, we don't have to... maybe numpy is smart enough to figure it out
		psin = psi.copy()
		
		
		#Interior points
		#psi[1:ny-1,1:nx-1] = psin[1:ny-1,1:nx-1]+dtau*(
		#		+(psin[1:ny-1,2:nx]-2*psin[1:ny-1,1:nx-1]+psin[1:ny-1,0:nx-2])/dx**2
		#		+(psin[2:ny,1:nx-1]-2*psin[1:ny-1,1:nx-1]+psin[0:ny-2,1:nx-1])/dy**2
		#		-zeta[1:ny-1,1:nx-1])
		
		#Jacobi interior
		eps = 0
		psi[1:ny-1,1:nx-1] = (1.0/4.0)*(psin[1:ny-1,2:nx]+psin[1:ny-1,0:nx-2]+psin[2:ny,1:nx-1]+psin[0:ny-2,1:nx-1])-(dx**2/4)*zeta[1:ny-1,1:nx-1]
		
		
		#x = 0 boundary
		#Jeg tror, vi skal tage et note ud af Holtons bog, og her, skipper vi psin[1:ny-1,-1] og bruger psin[1:ny-1,-2]
		#psi[1:ny-1,0] = psin[1:ny-1,0]+dtau*(
		#		+(psin[1:ny-1,1]-2*psin[1:ny-1,0]+psin[1:ny-1,-2])/dx**2
		#		+(psin[2:ny,0]-2*psin[1:ny-1,0]+psin[0:ny-2,0])/dy**2
		#		-zeta[1:ny-1,0])
		#Old
		#psi[1:ny-1,0] = psin[1:ny-1,0]+dtau*(
		#		+(psin[1:ny-1,1]-2*psin[1:ny-1,0]+psin[1:ny-1,-1])/dx**2
		#		+(psin[2:ny,0]-2*psin[1:ny-1,0]+psin[0:ny-2,0])/dy**2
		#		-zeta[1:ny-1,0])		
		
		#x = L boundary
		#Enten så gør den periodic sådan her
		#psi[1:ny-1,-1] = psi[1:ny-1,0]
		#eller sådan her, Holton
		#psi[:,-1] = psi[:,0]
		
		#Eller gør den periodic sådan her
		#psi[1:ny-1,-1] = psin[1:ny-1,-1]+dtau*(
		#+(psin[1:ny-1,0]-2*psin[1:ny-1,-1]+psin[1:ny-1,-2])/dx**2
		#+(psin[2:ny,-1]-2*psin[1:ny-1,-1]+psin[0:ny-2,-1])/dy**2
		#-zeta[1:ny-1,-1])
		
		#boundary at x = L, i'm gonna set equal to x = 0...
		#Boundary for psi, maybe i should remove these!
		psi[:,-1] = 0 #right boundary
		psi[:,0] = 0	#left boundary
		
		
		#What if i don't set it to 0? afaik it should be constant along the edges, but maybe not 0...
		#Det har i hvert fald bestemt en effekt om man sætter det til 0 eller ej..
		#Probably not needed to put it to 0, if I'm just careful the other places,
		#But, to follow the algorithm completely, I here set the y boundarys upper and lower to 0
		psi[0,:] = 0  #south boundary
		psi[-1,:] = 0 #north boundary
	
	
	#I think here, we should return psi, instead of doing it implicitly....
	#so, change the way the method works...
	return psi




def PsiSolvePoissonJacobi(psi,zeta,dx,dy,nx,ny,epstol,Ngc):
	"""
	Solve Poisson Equation
	Holton page 465
	
	psi is streamfunction
	zeta is vorticity
	
	nabla^2psi = zeta
	
	where we are solving for psi the streamfunction, and zeta is the relative vorticity
	
	
	hmm i think zeta is relative vorticity right, but we actually use another Zeta thing too???
	
	hmm... zeta er fatisk absolute vorticity
	og relative vorticity er Xi!
	hmm ok...
	Holton bruger faktisk zeta til absolut vorticity....
	Men, nogen steder siges det,
	Spørgsmålet er om poisson skal løses for
	nabla^2psi = xi
	eller
	nabla^2psi = zeta
	
	fordi, zeta = xi+f
	tror jeg...
	
	
	ahh, absolute vorticity i Holton er
	eta = zeta+f
	så zeta ER relative vorticity
	så (11.14) er aboslute vorticity
	og jeg tror indeed at (13.26) på en måde er set ud fra relative vorticity zeta, fordi at f part er sat i F(x,y,t)
	så det er nok fra absolute vorticity zeta+f, men så har man lavet det til en PDE for zeta
	
	
	
	
	
	
	We set BCs at y = top and y = bottom, but not x, i think
	Following lec12.pdf here
	
	
	From lec12.pdf,
	Solving poisson equation means putting some boundary condition on psi, right?
	Because otherwise you could add any constant to psi, and it would still be able to give some curvature
	nabla^2psi = f...
	so it makes sense, to give some unique solution, we impose boundary conditions, 
	but i think, for the sake of calculating velocity, it also wouldn't matter if we added some constant to psi
	
	
	right now i'm doing psi[1:ny-1,1:nx-1]
	#So that means i'm not setting psi[bottom,x] but I AM setting psi[top,x]
	#So i think it should be psi[1:ny-2,1:nx-1]
	#Or maybe, x should also be changed...
	But, remember in Python, 1:ny-1, then 1 is included, but ny-1 is excluded, so in effect, we're doing 1:ny-2
	
	
	
	Solve Poisson Equation,
	nabla^2psi = zeta
	Elliptic PDE
	It is the steady state solution of the pseudo-time problem,
	dpsi/dt = nabla^2psi - zeta
	
	FTCS = Forward Time, Centered Space
	
	#psi1[m,n] = psi[m,n]+dt/dx^2 (psi[m-1,n]+psi[m+1,n]+psi[m,n-1]+psi[m,n+1]-4psi[m,n])-dt*zeta[m,n]
	
	#stability requires, dt <= 1/4 * dx^2
	
	Jacobi Method is choosing dt = 1/4 * dx^2
	
	
	
	
	
	
	https://www.mi.uni-hamburg.de/arbeitsgruppen/theoretische-meteorologie/personen/lunkeit-frank/numerik/dokumente/barotrop.pdf
	nabla^2Ø - G0 = 0
	1) initial field, eg Ø = 0, which is what I have by psin = np.zeros()
	2) compute error e0 for each grid point... so it be practically an array...
	
	
	
	
	Should solve Poisson WITH beta plane?
	http://www.math.ualberta.ca/ijnam/Volume-10-2013/No-3-13/2013-03-04.pdf
	nabla^2psi = zeta-beta*y
	
	Både Holton og Durran de solver for nabla^2psi = zeta
	de solver for RELATIVE vorticity
	
	Yeah, jeg kan se, forskellige steder bruger forskellig notation.....
	http://empslocal.ex.ac.uk/people/staff/dbs202/cag/courses/MTMW14/notes2006.pdf
	her bruger de Xi til relative vorticity,
	men det er SAMME PDE system overall, det er så nabla^2psi = xi
	så, overall, er det altid nabla^2psi = relative vorticity
	
	
	
	Boundary Conditions
	Lec12, Dirichlet BCs psi = 0
	http://twister.caps.ou.edu/CFD2003/Phillips_NLInstablity.pdf
	at boundaries, psi=0 and xi=0 for all time
	
	http://empslocal.ex.ac.uk/people/staff/dbs202/cag/courses/MTMW14/notes2006.pdf
	Free-slip BCs at north and south, means v = 0, and du/dy = 0, 
	this leads to psi = constant and xi = 0 on north and south.
	
	

	"""
	#Compute streamfunction from vorticity
	#ζ_(i,j)^1=(((ψ_(i+1,j)-2ψ_(i,j)+ψ_(i-1,j) ))/dx^2 +((ψ_(i,j+1)-2ψ_(i,j)+ψ_(i,j-1) ))/dy^2 )

	#solve psi from lec12.pdf
	psin = np.zeros((ny,nx),dtype=np.float64)
	psin = psi.copy()
	
	#error betweeen iterated solution and RHS at each gridpoint
	eps = np.zeros((ny,nx),dtype=np.float64)
	
	#DO I NEED THIS???
	nabla2psi = np.zeros((ny,nx),dtype=np.float64)
	
	#I should, imo, be explicit and set BCs psi = 0....
	
	##JACOBI METHOD
	#dtau = 0.5*0.5*(0.5*dx**2+0.5*dy**2)
	nit = 0
	while True:
	#for r in range(500): #pseudo-time
	
		#update iteration counter
		nit +=1
		
		#Make copy of current iterate
		#We should probably do a copy, because, otherwise, we are doing intermediate changes...
		#i.e we are changing values that will be used later, that shouldn't....
		#So, that is, to really follow the algorithm, we need to copy the values...
		#At least, most likely... if it was a double for loop, then we would have to....
		#BUT, MAYBE, we don't have to... maybe numpy is smart enough to figure it out
		psin = psi.copy()
		
		
		
		#Calculate intermediate array
		#1/dx**2(psi[1:ny-1,2:nx]+psi[1:ny-1,0:nx-2]-2*psi[1:ny-1,1:nx-1]) +
		#1/dy**2(psi[2:ny,1:nx-1]+psi[0:ny-2,1:nx-1]-2*psi[1:ny-1,1:nx-1])
		nabla2psi[1+Ngc:ny-1-Ngc,Ngc+1:nx-1-Ngc]= ((1/dx**2)*(psi[1+Ngc:ny-1-Ngc,2+Ngc:nx-Ngc]
								+psi[1+Ngc:ny-1-Ngc,0+Ngc:nx-2-Ngc]-2*psi[1+Ngc:ny-1-Ngc,1+Ngc:nx-1-Ngc])
								+(1/dy**2)*(psi[2+Ngc:ny-Ngc,1+Ngc:nx-1-Ngc]
								+psi[0+Ngc:ny-2-Ngc,1+Ngc:nx-1-Ngc]-2*psi[1+Ngc:ny-1-Ngc,1+Ngc:nx-1-Ngc]))
		
		#Calculate error
		eps[1+Ngc:ny-1-Ngc,1+Ngc:nx-1-Ngc] = nabla2psi[1+Ngc:ny-1-Ngc,1+Ngc:nx-1-Ngc]-zeta[1+Ngc:ny-1-Ngc,1+Ngc:nx-1-Ngc]
		
		
		#Update iteration
		psi[1+Ngc:ny-1-Ngc,1+Ngc:nx-1-Ngc] = psin[1+Ngc:ny-1-Ngc,1+Ngc:nx-1-Ngc]+eps[1+Ngc:ny-1-Ngc,1+Ngc:nx-1-Ngc]/(2/dx**2+2/dy**2)
		
		
		#Interior points
		#psi[1:ny-1,1:nx-1] = psin[1:ny-1,1:nx-1]+dtau*(
		#		+(psin[1:ny-1,2:nx]-2*psin[1:ny-1,1:nx-1]+psin[1:ny-1,0:nx-2])/dx**2
		#		+(psin[2:ny,1:nx-1]-2*psin[1:ny-1,1:nx-1]+psin[0:ny-2,1:nx-1])/dy**2
		#		-zeta[1:ny-1,1:nx-1])
		
		
		#https://www.mi.uni-hamburg.de/arbeitsgruppen/theoretische-meteorologie/personen/lunkeit-frank/numerik/dokumente/barotrop.pdf
		#psi[1:ny-1,1:nx-1] = ((1/dx**2)*(psi[1:ny-1,2:nx]+psi[1:ny-1,0:nx-2]-2*psi[1:ny-1,1:nx-1])
		#						+(1/dy**2)*(psi[2:ny,1:nx-1]+psi[0:ny-2,1:nx-1]-2*psi[1:ny-1,1:nx-1])
		#						-zeta[1:ny-1,1:nx-1])/(2/dx**2+2/dy**2)
		
		
		
		#Jacobi interior
		#psi[1:ny-1,1:nx-1] = ((1.0/4.0)*(
		#						+psin[1:ny-1,2:nx]
		#						+psin[1:ny-1,0:nx-2]
		#						+psin[2:ny,1:nx-1]
		#						+psin[0:ny-2,1:nx-1])
		#					-(dx**2/4)*zeta[1:ny-1,1:nx-1])
		
		
		#x = 0 boundary
		#Jeg tror, vi skal tage et note ud af Holtons bog, og her, skipper vi psin[1:ny-1,-1] og bruger psin[1:ny-1,-2]
		#psi[1:ny-1,0] = psin[1:ny-1,0]+dtau*(
		#		+(psin[1:ny-1,1]-2*psin[1:ny-1,0]+psin[1:ny-1,-2])/dx**2
		#		+(psin[2:ny,0]-2*psin[1:ny-1,0]+psin[0:ny-2,0])/dy**2
		#		-zeta[1:ny-1,0])
		#Old
		#psi[1:ny-1,0] = psin[1:ny-1,0]+dtau*(
		#		+(psin[1:ny-1,1]-2*psin[1:ny-1,0]+psin[1:ny-1,-1])/dx**2
		#		+(psin[2:ny,0]-2*psin[1:ny-1,0]+psin[0:ny-2,0])/dy**2
		#		-zeta[1:ny-1,0])		
		
		#x = L boundary
		#Enten så gør den periodic sådan her
		#psi[1:ny-1,-1] = psi[1:ny-1,0]
		#eller sådan her, Holton
		#psi[:,-1] = psi[:,0]
		
		#Eller gør den periodic sådan her
		#psi[1:ny-1,-1] = psin[1:ny-1,-1]+dtau*(
		#+(psin[1:ny-1,0]-2*psin[1:ny-1,-1]+psin[1:ny-1,-2])/dx**2
		#+(psin[2:ny,-1]-2*psin[1:ny-1,-1]+psin[0:ny-2,-1])/dy**2
		#-zeta[1:ny-1,-1])
		
		
		
		
		#Psi no-flow across boundary GHOST CELLS
		#boundary at x = L, i'm gonna set equal to x = 0...
		#Boundary for psi, maybe i should remove these!
		psi[:,-1] = 0 #right boundary
		psi[:,0] = 0	#left boundary
		
		
		#What if i don't set it to 0? afaik it should be constant along the edges, but maybe not 0...
		#Det har i hvert fald bestemt en effekt om man sætter det til 0 eller ej..
		#Probably not needed to put it to 0, if I'm just careful the other places,
		#But, to follow the algorithm completely, I here set the y boundarys upper and lower to 0
		psi[0,:] = 0  #south boundary
		psi[-1,:] = 0 #north boundary
		
		
		#Psi no-flow across boundary ACTUAL BOUNDARY
		psi[:,-1+Ngc] = 0 #right boundary
		psi[:,0+Ngc] = 0	#left boundary
		psi[0+Ngc,:] = 0  #south boundary
		psi[-1-Ngc,:] = 0 #north boundary
		
		#
		
		#No-slip psi streamfunction BC
		#Maybe I need additional BCs due to the no-slip condition??
		#no-slip, hence, on sourthern boundary,
		#hence, u0 = 0 on sourthern boundary, and ALSO v0 = 0 on sourthern boundary
		#now, u0 = 0, but, u1 != 0 likely...
		#so, on southern boundary, there would be, du/dy...
		#hence, there WOULD be a psi and a zeta, right?
		#ie, for no-slip, then zeta is NOT zero right, at boundary?
		#yep... for no-slip, zeta is NOT zero at boundary, and i think, psi is ALSO a bit more complicated
		#maybe,
		#psi[:,1] = psi[:,0]+u[:,0]*dy
		#something like that..
		#actually hmm it might be good enough.... i actually think it's okay,
		#psi[:,1] will come from solving poisson equation, 
		
		
		#But, should maybe plot the solution... to see if the boundaries are somewhat satisfied...
		#so make a 3d plot of the psi field...
		
		
		#lec12, on sourthern boundary, n = (0,1), hence nablapsi.n = 0 = dpsi/dy = 0
		#yeah... that will give, u = -dpsi/dy = 0 on boundary....
		#but that almost means, that, it should be, psi0 = psi1 = 0...
		#like, psi0,i = psi1,i = 0...
		#So i should actually enfore the psi to be zero even further out, i THINK...
		#because ONE thing is ghost cells, those are not the ACTUAL boundary, i think...
		#they are a pseudo-boundary... the ACTUAL boundary is even further inside,
		#so i think i need to enfore psi = 0 even further inside that what i currently have...
		#also, hence, the Poisson solver, should actually solve LESS area than what it doesn
		#I need to reduce the area by +-1 in each direction i think...
		#like, there's BOUNDARY conditions, AND, ghost cell conditions...
		#so just think like, psi[:,0] is not an ACTUAL BOUNDARY condition, it's actually a GHOST CELL CONDITION
		#so i need to ALSO set psi[:,1] as the ACTUAL boundary condition, AND change the algorithms...
		


		#so... if i want u = 0 on southern boundary, I would need,
		#u = 0 = -(psi(1)-psi(-1))/dy
		#so maybe I DO need ghost cells or something...
		#and then I would have psi(-1) = psi(0) = 0
		#psi(0) = 0 from dirichlet psi = 0 condition on BCs
		#psi(-1) = 0 from no-slipp conditions...
		#
		#Like, det er lidt som, it's a bit like,
		#hvis man har en vorticity-streamfunction formulation
		#så SKAL man jo nærmest have en staggered grid?
		#almost JUST HAPPENS to be that way...
		#because, u = dpsi/dx... so... it's like... i mean maybe you could FORCE it to be unstaggered,
		#but, by it's very nature, it seems staggered
		#so, how do we deal with that then??
		
		
		#psi[:,-1-1] = 0 #right boundary
		#psi[:,0+1] = 0	#left boundary
		#psi[0+1,:] = 0  #south boundary
		#psi[-1-1,:] = 0 #north boundary
		
		
		#Now me tihnking, ghost cells or just complicated boundary conditions?
		#Well actually, ghost cells are also used in eg Semi-Lagrangian CFD...
		#so, it's actually maybe rather common in some ways...
		#and it also speaks to the idea of simulating a larger domain, it's sort of same philosophy
		#so imo, might aswell just get used to it, and start adding ghost cells a bit here...
		#
		
		

		
		#print(eps)
		if (np.abs(eps) < epstol).all():
			print("Break Poisson algorithm at", nit)
			break
		
		
	
	#I think here, we should return psi, instead of doing it implicitly....
	#so, change the way the method works...
	return psi




def Jacobian(u,v,zeta,psi,beta):
	"""
	To update relative vorticity zeta

	J(p,q) = dp/dx * dq/dy - dp/dy * dq/dx

	One approximation is,
	Jhat(p,q) = (d2xp)(d2yq)-(d2yp)(d2xq)


	For BVE, J(psi, nabla^2psi)
	So, that corresponds to using u,v and zeta = nabla^2psi


	Also, it should probably actually be,
	Lec12,
	J(psi, f+zeta)
	#So, maybe J(psi, f + nabla^2psi)???


	"""

	#I think these are Flux version tbh
	Fmn = (\
		(u[1:ny-1,2:nx]*zeta[1:ny-1,2:nx]-u[1:ny-1,0:nx-2]*zeta[1:ny-1,0:nx-2])/(2*dx)\
		+(v[2:ny,1:nx-1]*zeta[2:ny,1:nx-1]-v[0:ny-2,1:nx-1]*zeta[0:ny-2,1:nx-1])/(2*dy)\
		+beta*v[1:ny-1,1:nx-1])



	# #Arakawa Jacobian
	# Ja = np.zeros((ny,nx))

	# #I think actually, for Arakawa Jacobian, we need stream function psi,
	# #and not JUST the u,v velocities that come from psi


	# #temp2 will have psi*zeta terms???
	# temp1 = (1/3)*(u[1:ny-1,1:nx-1]*zeta[2:ny,1:nx-1]-v[1:ny-1,1:nx-1]*zeta[1:ny-1,2:nx])*(1/(2*dx*2*dy))
	# temp2 = (1/3)*(psi[
	# temp3 = 0
	# #each term in each (1/3) term, will have 1/(2dx2dy) factor i'm pretty sure
	# Ja[1:ny-1,1:nx-1] = temp1+temp2+temp3



	return Fmn
	
	
	
def ArakawaJacobian():
	"""
	To update relative vorticity zeta
	
	J(p,q) = dp/dx * dq/dy - dp/dy * dq/dx
	
	One approximation is,
	Jhat(p,q) = (d2xp)(d2yq)-(d2yp)(d2xq)
	
	
	For BVE, J(psi, nabla^2psi)
	So, that corresponds to using u,v and zeta = nabla^2psi
	
	
	Also, it should probably actually be,
	Lec12,
	J(psi, f+zeta)
	#So, maybe J(psi, f + nabla^2psi)???
	
	
	"""
	
	#I think these are Flux version tbh
	Fmn = (\
		(u[1:ny-1,2:nx]*zeta[1:ny-1,2:nx]-u[1:ny-1,0:nx-2]*zeta[1:ny-1,0:nx-2])/(2*dx)\
		+(v[2:ny,1:nx-1]*zeta[2:ny,1:nx-1]-v[0:ny-2,1:nx-1]*zeta[0:ny-2,1:nx-1])/(2*dy)\
		+beta*v[1:ny-1,1:nx-1])
	
	
	
	# #Arakawa Jacobian
	# Ja = np.zeros((ny,nx))
	
	# #I think actually, for Arakawa Jacobian, we need stream function psi,
	# #and not JUST the u,v velocities that come from psi
	
	
	# #temp2 will have psi*zeta terms???
	# temp1 = (1/3)*(u[1:ny-1,1:nx-1]*zeta[2:ny,1:nx-1]-v[1:ny-1,1:nx-1]*zeta[1:ny-1,2:nx])*(1/(2*dx*2*dy))
	# temp2 = (1/3)*(psi[
	# temp3 = 0
	# #each term in each (1/3) term, will have 1/(2dx2dy) factor i'm pretty sure
	# Ja[1:ny-1,1:nx-1] = temp1+temp2+temp3



	return 0




def nabladotv(u,v,nx,ny,dx,dy):
	"""
	#divergne should be 0??? right?? so calculate it and plot!
	Should maybe be centered differences??
	"""
	
	
	divv = (u[:,1:nx-1]-u[:,0:nx-2])/dx + (v[1:ny-1,:]-v[0:ny-2,:])/dy

	return divv

def RobertAsselinFilter():
	"""
	Often used with Leap-frog scheme
	http://weather.ou.edu/~ekalnay/NWPChapter3/Ch3_2_4.html
	
	
	"""


	return psi



def CalcVelocity(psi,dx,dy):
	"""
	Should probably also take u,v as input, or initiate u,v here...
	ug,vg geostrophic
	
	ug = -dpsi/dy
	vg = dpsi/dx
	
	these velocities depend on streamfunction psi being correct, especially near BCs...
	BCs are set outside a bit...
	#so v[0,:] eg is outside this function...
	
	
	"""
	
	#psi[y,x] array order
	for i in range(1,nx-1):
		for j in range(1,ny-1):
			u[i,j] = -(psi[i+1,j]-psi[i-1,j])/(2*dy)
			v[i,j] = (psi[i,j+1]-psi[i,j-1])/(2*dx)
			
			
	return u,v

if __name__ == "__main__":

	import numpy as np
	#from pylab import *
	import matplotlib.pyplot as plt
	import matplotlib.animation as animation
	from mpl_toolkits.mplot3d import axes3d

	
	
	print("ARRAY TEST")
	atest = np.zeros((4,4))-3
	print(np.abs(atest))
	if (atest<4).all():
		
		print("ths works .all()")
		
	if (atest<4).any():
		print("ths works .any()")
	
	

	Lx = 6000 #km
	Ly = 6000 #km
	nx = 65
	ny = 65
	pi = 3.141592
	#x = np.linspace(0,Lx,nx)
	#y = np.linspace(0,Ly,ny)
	X = np.linspace(-Lx/2,Lx/2,nx)
	Y = np.linspace(-Ly/2,Ly/2,ny)
	x,y = np.meshgrid(X*1000,Y*1000)
	k = 2*pi/(Lx*1000)
	m = pi/(Ly*1000)
	dx = 1000*Lx/(nx-1)
	dy = 1000*Ly/(ny-1)
	U0 = 20				#zonal wind
	beta = 1e-11#1.62*10**(-11)	#he set 0 infront?
	Av4 = 10**(-6)
	A = 10**(-4)
	#initial vorticity and streamfunction
	
	
	#Poisson solver error
	epstol = 1e-7


	#We have 3 sets of zetas here, one is initial, I would assume? zeta0
	#zeto0 is set to a gaussian it
	zeta0 = np.array(A*np.exp(-2*(k**2*x**2+m**2*y**2)),dtype=np.float64)
	zeta = zeta0.copy()
	zetan = zeta0.copy()



	#time integration parameters					#hours
	time_end = 3*3600 				#seconds
	dt = 100 #seconds
	t = 0

	psi = np.zeros((ny,nx),dtype=np.float64)
	dypsi = np.zeros((ny,nx),dtype=np.float64)
	dxpsi = np.zeros((ny,nx),dtype=np.float64)
	u = np.zeros((ny,nx),dtype=np.float64)
	v = np.zeros((ny,nx),dtype=np.float64)
	#dfly = np.zeros((ny,nx),dtype=np.float64)
	#dflx = np.zeros((ny,nx),dtype=np.float64)

	
	#Ghost cells
	Ngc = 0
	

	while t < time_end:
		
		print(t)
		
		t+= dt
		
		#Calculate streamfunction psi
		psi = PsiSolvePoissonJacobi(psi,zeta,dx,dy,nx,ny,epstol,Ngc)
		
		#psi = psi + U0*(Ly/2*1000 -y)




		#calculating velocities
		#only in interior
		u,v = CalcVelocity(psi,dx,dy)
		
		#f[y,x], boundary conditions for velocity
		#no-flow across boundary
		u[:,0] = 0 #western border
		u[:,-1] = 0 #eastern border
		v[0,:] = 0 #southern border
		v[-1,:] = 0 #northern border
		
		#no slip,
		u[0,:] = 0 #southern border
		u[-1,:] = 0 #northern border
		v[:,0] = 0 #western border
		v[:,-1] = 0 #eastern border
		

		
		
		#Actually, maybe already HERE; i should put in BCs...
		#because Jacobian will use them!...
		
		#Maybe also BCs before first timestep... like maybe plot initial zeta....
		#as 3dplot...
		#check, how FAST does the instability grow?
		#Is it already after 2nd step iteration???
		#because maybe i should do it BEFORE poisson equation too, since poisson equation will use Zeta...
		#also, try to look at psi solution, from lower z-vertical value......
		#because maybe i can't see if there's a problem in psi, due to scaling of vertical plot axis...
		#so try to change axis....
		#maybe psi actually DOES have also a discontinuity instability at the edge, but it's just very SMALL
		#compared to the large inner mountain peak....
		#so it LOOOKs like boudnary is basically smooth at zero, but inreality, if we zoom in,
		#maybe psi is also kinda fucked near edges....
		

		#zeta Boundary Conditions 
		#Here I haven't set boundary conditions yet..

		#according to https://www.mi.uni-hamburg.de/arbeitsgruppen/theoretische-meteorologie/personen/lunkeit-frank/numerik/dokumente/barotrop.pdf
		#maybe I can get their result from the jacobian too??
		
		#Full-slip zeta BC
		#since u0=u1 and uNY=uNY+1, zeta = -du/dy = 0 on northern and southern BCs
		#zeta[0,:] = 0 #south
		#zeta[-1,:] = 0 #north
		#zeta[:,0] = 0 #west
		#zeta[:,-1] = 0 #east
		
		
		#No-slip zeta BC
		#GHOST CELLS OR BOUNDARY???
		#zeta = -du/dy
		#dv/dx = 0, because v = 0, due to no-flow across boundary
		#south, along the entire edge
		zeta[0,:] = (2/dy**2)*(psi[1,:]-psi[0,:])
		#zeta[0,:] = -(u[1,:]-u[0,:])/dy #south
		#north, along the entire edge
		zeta[-1,:] = (2/dy**2)*(psi[-1,:]-psi[-2,:])
		#zeta[-1,:] = -(u[-1,:]-u[-2,:])/dy #north
		
		
		#zeta = dv/dx
		#-du/dy = 0, because u = 0, due to no-flow across boundary
		#west, along entire egde
		zeta[:,0] = (2/dx**2)*(psi[:,1]-psi[:,0]) #west
		#zeta[:,0] = (v[:,1]-v[:,0])/dx #west
		#east along entire edge
		zeta[:,-1] = (2/dx**2)*(psi[:,-1]-psi[:,-2]) #east
		#zeta[:,-1] = (v[:,-1]-v[:,-2])/dx #east
		
		
		
		#2nd version no-slip BC condition on vorticity
		#https://web.math.princeton.edu/~weinan/papers/cfd5.pdf
		#zeta[0,:] = (2/dy**2)*psi[1,:]
		#zeta[-1,:] = (2/dy**2)*psi[-2,:] #maybe this one should have -minus infront??
		
		#zeta[:,0] = (2/dx**2)*psi[:,1]
		#zeta[:,-1] = (2/dx**2)*psi[:,-2] #maybe this one should have -minus infront??
		
		#Free-slip BCs (also called full-slip sometimes, i think)
		#https://www.mi.uni-hamburg.de/arbeitsgruppen/theoretische-meteorologie/personen/lunkeit-frank/numerik/dokumente/barotrop.pdf
		#u0 = u1 and uNY+1 = uNY
		#aka, on north and south, velocity is not zero,
		
		
		#No-flow across boundary
		#https://www.mi.uni-hamburg.de/arbeitsgruppen/theoretische-meteorologie/personen/lunkeit-frank/numerik/dokumente/barotrop.pdf
		#on north and south, v = 0
		#then psi0 = psiNY+1 = constant in x, 





		#Updating relative vorticity zeta
		#forward euler, should be leapfrog
		#Fmn = (\
		#	(u[1:ny-1,2:nx]*zeta[1:ny-1,2:nx]-u[1:ny-1,0:nx-2]*zeta[1:ny-1,0:nx-2])/(2*dx)\
		#	+(v[2:ny,1:nx-1]*zeta[2:ny,1:nx-1]-v[0:ny-2,1:nx-1]*zeta[0:ny-2,1:nx-1])/(2*dy)\
		#	+beta*v[1:ny-1,1:nx-1])
		Fmn = Jacobian(u,v,zeta,psi,beta)
		integralFmn = np.sum(Fmn)
		print("Fmn integral ",integralFmn)
		
		

		zeta[1:ny-1,1:nx-1] = zeta[1:ny-1,1:nx-1] - dt*Fmn

		print("zeta S edge", zeta[0,0:4])
		print("zeta N edge", zeta[-1,0:4])
		print("psi S+1 edge", psi[1,0:4])
		print("psi N-1 edge", psi[-2,0:4])
		
	#initial streamfunction
	psi0 = PsiSolvePoissonJacobi(psi,zeta0,dx,dy,nx,ny,epstol,Ngc)
	
	u0,v0 = CalcVelocity(psi0,dx,dy)
	
	
	
	#plot poisson solution of nabla^2psi = zeta
	fig00 = plt.figure() #If i do pcolor, then no need for 3d projection
	ax00 = fig00.gca(projection='3d')
	ax00.plot_surface(x, y, psi0)#, rstride=3, cstride=3, color='black')
	ax00.set_title('Psi from Poisson nabla2psi = xi')
	ax00.set_xlabel('x')
	ax00.set_ylabel('y')
	plt.show()
	
	

	#plot initial conditions
	fig0 = plt.figure(1)
	ax0 = plt.gca()
	ax0.set_title('Barotropic Vorticity Equation Initial configuraton')
	ax0.set_xlabel('x')
	ax0.set_ylabel('y')
	#ax.quiver(x/1000,y/1000,u,v)
	#C = ax0.contour(x/1000,y/1000,zeta0*10**7,8,colors='black')
	C = ax0.contour(x/1000,y/1000,zeta0,8,colors='black')
	C = ax0.contour(x/1000,y/1000,psi0,4,colors='black')
	plt.clabel(C, fontsize=10, inline=1,fmt = '%1.0f')
	ax0.quiver(x/1000,y/1000,u0,v0)
	plt.savefig('BVEboundingboxinitial.png')
	plt.show()



	#plt.switch_backend('QT4Agg')
	fig = plt.figure(2)
	ax = plt.gca()
	ax.set_title('Barotropic Vorticity Equation final config')
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	#ax.quiver(x/1000,y/1000,u,v)
	#C = ax.contour(x/1000,y/1000,zeta*10**7,8,colors='black')
	Czeta = ax.contour(x/1000,y/1000,zeta,6,colors='black')
	Cpsi = ax.contour(x/1000,y/1000,psi,4,colors='black')
	plt.clabel(Czeta, fontsize=10, inline=1)#,fmt = '%1.0f')
	plt.clabel(Cpsi, fontsize=10, inline=1)#,fmt = '%1.0f')
	ax.quiver(x/1000,y/1000,u,v)
	plt.savefig('BVEboundingboxfinal.png')
	plt.show()
	
	
	#plot zeta final
	fig01 = plt.figure() #If i do pcolor, then no need for 3d projection
	ax01 = fig01.gca(projection='3d')
	ax01.plot_surface(x, y, zeta)#, rstride=3, cstride=3, color='black')
	ax01.set_title('Zeta final')
	ax01.set_xlabel('x')
	ax01.set_ylabel('y')
	plt.show()
	
		
	#plot psi final
	fig01 = plt.figure() #If i do pcolor, then no need for 3d projection
	ax01 = fig01.gca(projection='3d')
	ax01.plot_surface(x, y,psi)#, rstride=3, cstride=3, color='black')
	ax01.set_title('psi final')
	ax01.set_xlabel('x')
	ax01.set_ylabel('y')
	plt.show()
	
	
	

	fig2 = plt.figure(3)
	ax2 = plt.gca()
	ax2.set_title('Barotropic Vorticity Equation')
	ax2.set_xlabel('x')
	ax2.set_ylabel('y')
	#ax.quiver(x/1000,y/1000,u,v)
	#C = ax.contour(x/1000,y/1000,zeta0*10**7,8,colors='black')
	ax2.quiver(x/1000,y/1000,u,v)
	plt.show()


