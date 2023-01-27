import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import serviceData from '../Services/serviceData';
import Image from 'react-bootstrap/Image'




export default function AppService()
{

    return(
    <section id ="services" className='block services-block'>
     <Container fluid>
        <div className='title-holder'>

            <h2>Our Services</h2>
            <div className='subtitle'>
                What we do.

            </div>
        </div>
      <Row>
        {
            serviceData.map(service=>{
                return(
        <Col sm={4} className="holder" key={service.id}>
        <div className="icon">
            <Image src=  {service.icon} /></div>

            <h3>{service.header}</h3>
            <p>{service.content}</p>

        
        </Col>
                    )
            })
        }
        
      </Row>
    </Container>

    </section>    )
}