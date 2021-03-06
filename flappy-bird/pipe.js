class Pipe {
  constructor() {
    this.spacing = 200
    this.top = random(height/6, 3/4 *height)
    this.bottom = height - (this.top + this.spacing)
    this.x = width 
    this.w = 50
    this.speed = 3
    this.highlight = false
  }

  show () {
    fill(255)
    if (this.highlight) {
      fill(255,0,0)
    }
    rect(this.x, 0, this.w, this.top)
    rect(this.x, height-this.bottom, this.w, this.bottom)
    
  }

  update () {
    this.x -= this.speed
  }

  hits (bird) {
    if (bird.y < this.top || bird.y > height - this.bottom) {
      if (bird.x > this.x && bird.x < this.x + this.w) {
        this.highlight = true
        return true
      }
    }
    if (bird.y == height || bird.y == 0) {
      return true
    }
    this.highlight = false  
    return false
  }

  offscreen () {
    if (this.x < -this.w) {
      return true
    } else {
      return false
    }
  }
}