import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Image from 'react-bootstrap/Image'
import img1 from '../assets/images/img1.jpg'


export default function AppAbout(){
    return(
        <section id ="about" className="block about-block">
            <Container fluid>
                <div className="title-holder"> 
                <h2>About Us</h2>
                <div className='subtitle'>Learn more about us</div>
                </div>
        <Row>
          <Col sm={6}>
            <Image src={img1}/>
          </Col>

          <Col sm={6}><p>GCM has worked across many industries, and we know the intricacies of retail, office, hotels, education, and institutional projects. In addition, we have worked on new construction, renovations and tenant improvements. We understand the needs of business owners, contractors, brokers, developers, and landlords.</p>
          
          <p>We have the ability to assemble a custom team to tackle any project, large or small, but you will always have one contact to make sure your project needs are being met.

</p></Col>

        </Row>
      </Container>



        </section>
        
    )
}