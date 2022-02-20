import React, {useEffect, useState} from 'react';
import './App.css';

function App() {
  const [colorValue, setColorValue] = useState('#000000')
  const [RGBValue, setRGBValue] = useState('rgb(0, 0, 0)')
  const [CMYKValue, setCMYKValue] = useState('cmyk(0%, 0%, 0%, 100%)')
  const [HLSValue, setHLSValue] = useState('hls(0, 0%, 0%)')

  const [RGBValid, setRGBValid] = useState(true)
  const [CMYKValid, setCMYKValid] = useState(true)
  const [HLSValid, setHLSValid] = useState(true)

  const [editing, setEditing] = useState(null)

  useEffect(() => {
    if (editing == null)
      return

    let rgb = hexToRgb(colorValue)
    let cmyk = rgbToCmyk(rgb.r, rgb.g, rgb.b)
    let hls = rgbToHls(rgb.r, rgb.g, rgb.b)
    
    if (editing != 'rgb')
      setRGBValue(`rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`)
    if (editing != 'cmyk')
      setCMYKValue(`cmyk(${cmyk.c}%, ${cmyk.m}%, ${cmyk.y}%, ${cmyk.k}%)`)
    if (editing != 'hls')
      setHLSValue(`hls(${hls.h}, ${hls.l}%, ${hls.s}%)`)
  }, [colorValue])

  const hexToRgb = (hex) => {
    let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null;
  }
  
  const rgbToHex= (r, g, b) => {
    const componentToHex = (c) => {
      let hex = c.toString(16);
      return hex.length == 1 ? "0" + hex : hex;
    }

    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
  }

  const cmykToRgb = (c, m, y, k) => {
    return {
      r: Math.round(255 * (1 - c) * (1 - k)),
      g: Math.round(255 * (1 - m) * (1 - k)),
      b: Math.round(255 * (1 - y) * (1 - k))
    }
  }

  const rgbToCmyk = (r, g, b) => {
    let k = Math.min(1 - r / 255, 1 - g / 255, 1 - b / 255)
    return {
      c: Math.round(100 * (1 - r / 255 - k) / (1 - k)),
      m: Math.round(100 * (1 - g / 255 - k) / (1 - k)),
      y: Math.round(100 * (1 - b / 255 - k) / (1 - k)),
      k: Math.round(100 * k)
    }
  }

  const hlsToRgb = (h, l, s) => {
    l /= 100
    s /= 100

    let c = (1 - Math.abs(2 * l - 1)) * s
    let x = c * (1 - Math.abs(Math.floor(h / 60) % 2 - 1))
    let m = l - c / 2

    let arr = [[c, x, 0], [x, c, 0], [0, c, x], [0, x, c], [x, 0, c], [c, 0, x]]
    let [r, g, b] = arr[Math.floor(h / 60)]
    
    return {
      r: Math.round(255 * (r + m)),
      g: Math.round(255 * (g + m)),
      b: Math.round(255 * (b + m))
    }
  }

  const rgbToHls = (r, g, b) => {
    r /= 255
    g /= 255
    b /= 255

    let cMax = Math.max(r, g, b)
    let cMin = Math.min(r, g, b)
    let delta = cMax - cMin

    let h, l, s

    if (delta === 0)
      h = 0
    else if (cMax === r)
      h = 60 * (((g - b) / delta) % 6)
    else if (cMax === g)
      h = 60 * ((b - r) / delta + 2)
    else
      h = 60 * ((r - g) / delta + 4)
    
    l = (cMax + cMin) / 2

    s = delta / (1 - Math.abs(2 * l - 1))

    h = Math.round(h)

    return {
      h: h < 0 ? 360 + h : h,
      l: Math.round(100 * l),
      s: Math.round(100 * s)
    }
  }

  const colorInput = (e) => {
    setColorValue(e.target.value)
    setEditing('none')
  }

  return (
    <div className="App">
      <h1>RGB, CMYK, HLS</h1>
      <div>
        <input type='color' value={colorValue} onInput={colorInput}/>
      </div>
      <div>
        <span>RGB</span>
        <input type='text' className={`${!RGBValid ? 'error' : ''}`} value={RGBValue} onChange={(e) => {
          setRGBValue(e.target.value)
          setEditing('rgb')

          let splited = /^rgb\(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\s*,\s*([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\s*,\s*([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\s*\)$/.exec(e.target.value);
          
          if (splited === null) {
            setRGBValid(false);
            return
          }
          setRGBValid(true);

          splited = splited.map((x) => parseInt(x))
          setColorValue(rgbToHex(splited[1], splited[2], splited[3]))
          }}/>
      </div>
      <div>
        <span>CMYK</span>
        <input type='text' className={`${!CMYKValid ? 'error' : ''}`} value={CMYKValue} onChange={(e) => {
          setCMYKValue(e.target.value)
          setEditing('cmyk')

          let splited = /^cmyk\(([0-9]|[1-9][0-9]|100)%\s*,\s*([0-9]|[1-9][0-9]|100)%\s*,\s*([0-9]|[1-9][0-9]|100)%\s*,\s*([0-9]|[1-9][0-9]|100)%\s*\)$/.exec(e.target.value);
          
          if (splited === null) {
            setCMYKValid(false);
            return
          }
          setCMYKValid(true);

          splited = splited.map((x) => parseInt(x) / 100)
          let rgb = cmykToRgb(splited[1], splited[2], splited[3], splited[4])
          
          setColorValue(rgbToHex(rgb.r, rgb.g, rgb.b))
          }}/>
      </div>
      <div>
        <span>HLS</span>
        <input type='text' className={`${!HLSValid ? 'error' : ''}`} value={HLSValue} onChange={(e) => {
          setHLSValue(e.target.value)
          setEditing('hls')
          
          let splited = /^hls\(([0-9]|[1-9][0-9]|[12][0-9]{2}|3[0-5][0-9])\s*,\s*([0-9]|[1-9][0-9]|100)%\s*,\s*([0-9]|[1-9][0-9]|100)%\s*\)$/.exec(e.target.value)
          
          if (splited === null) {
            setHLSValid(false);
            return
          }
          setHLSValid(true);

          splited = splited.map((x) => parseInt(x))
          let rgb = hlsToRgb(splited[1], splited[2], splited[3])
          
          setColorValue(rgbToHex(rgb.r, rgb.g, rgb.b))
          }}/>
      </div>
    </div>
  );
}

export default App;
