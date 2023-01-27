import Carousel from 'react-bootstrap/Carousel';
import heroData from '../Services/heroData';

export default function AppHero(){
    return (
   <section id="home" className='hero-block'>
     <Carousel>
        {
            heroData.map(hero=>{
                return(
                    <Carousel.Item key={hero.id}>
                    <img
                      className="d-block w-100"
                      src={hero.image}
                      alt={"Slide "+hero.id}
                    />
                    <Carousel.Caption>
                      <h3>{hero.title}</h3>
                      <p>{hero.description}</p>
                      <a className='btn btn-primary' href = "#works">View Gallery</a>
                    </Carousel.Caption>
                    </Carousel.Item>
                )
                
            })
        }
            
    </Carousel>
    </section>
    )
}


