# newton_fractal
Draw beautiful fractals derived from Newton-Raphson iteration. Based on [this](http://code.activestate.com/recipes/577166-newton-fractals/) python recipe.

## Feautures
- create png or animated gif file of fractal
- polynomial can be given with its roots or coefficients
- fractals colored by root reached and shaded by rate of convergence, the completely black points do not converge at all

## Usage
Import the python file
```python
import newton_fractal as nf
```

### Crete polynomial
Crate polynomial x(x-1)(x-2)(x-3) with its roots
```python
p = nf.Polynomial([0, 1, 2, 3], 'roots')
```
Crate polynomial (3i)x^3^+(-2+i)x^2^-1 with complex coefficients
```python
p = nf.Polynomial([3j, -2+1j, 0, -1], 'coefficients')
```

### Draw fractal
Let assume p is a polynomial created the way it is described above, and we want to create a picture of it in the complex space. The following parameters needed in order:
- bottom-left corner (on the complex space)
- top-right corner
- width (number of pixels and complex numbers where the iteration will be started)
- height
- file name (without extension)
```python
p.draw_fractal(-20-10j, 20+10j, 400, 100, "fractal")
```

### Create animated gif
Let assume p is a polynomial created the way it is described above, and we want to create a sequence of pictures of it and merge them to a single gif file. The following parameters needed in order:
- bottom-left corner of the first picture (on the complex space)
- top-right corner of the first picture
- bottom-left corner of the last picture
- top-right corner of the last picture
- width (number of pixels and complex numbers where the iteration will be started)
- height
- number of frames in gif
- file name (without extension)
```python
p.animate_fractal(-20-10j, 20+10j, -2-1j, 2+1j, 400, 100, 20, "fractal")
```

## Examples
Create the examples found on [Wikipedia](https://en.wikipedia.org/wiki/Newton_fractal)
```python
nf.Polynomial([1,0,0,-1], 'coefficients').draw_fractal(-10-10j, 10+10j, 400, 400, 'example_1')
nf.Polynomial([1,0,-2,2], 'coefficients').draw_fractal(-10-10j, 10+10j, 400,400, 'example_2')
nf.Polynomial([1,0,0,0,15,0,0,0,-16], 'coefficients').draw_fractal(-2-2j, 2+2j, 400, 400, 'example_3')
```

![example_1](https://raw.githubusercontent.com/muchaco/newton_fractal/master/examples/example_1.png)
![example_2](https://raw.githubusercontent.com/muchaco/newton_fractal/master/examples/example_2.png)
![example_3](https://raw.githubusercontent.com/muchaco/newton_fractal/master/examples/example_3.png)

```python
nf.Polynomial([1,0,0,-1], 'coefficients').animate_fractal(-10-10j, 10+10j, -1-1j, 1+1j, 400, 400, 20, 'example_1')
nf.Polynomial([1,0,-2,2], 'coefficients').animate_fractal(-10-10j, 10+10j, 9-0.5j, 10+0.5j, 400, 400, 20, 'example_2')
```

![example_1](https://raw.githubusercontent.com/muchaco/newton_fractal/master/examples/example_1.gif)
![example_2](https://raw.githubusercontent.com/muchaco/newton_fractal/master/examples/example_2.gif)
