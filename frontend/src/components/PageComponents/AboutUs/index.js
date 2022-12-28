import { AboutUsText } from './AboutUsElements';
import {
  SingleElementContainer,
  ColumnContainerBasic,
  GraphicContainer,
  GraphicImg,
} from '../../Common/ContainerElements';
import { FormTitle } from '../../Common/FormElements';
import { ExternalLink } from '../../Common/UserContentElements';

import graphic from '../../../images/about_us.jpg';

const AboutUs = () => {
  return (
    <>
      <SingleElementContainer>
        <ColumnContainerBasic>
          <GraphicContainer>
            <GraphicImg src={graphic} />
          </GraphicContainer>
          <FormTitle>About us</FormTitle>
          <AboutUsText>
            I developed this application to provide web developers with the tools to
            improve SEO on their websites. Send a message on
            <ExternalLink
              href='https://github.com/vkiguta/seo-saver'
              target='_blank'>
              https://github.com/vkiguta/seo-saver
            </ExternalLink>
          </AboutUsText>
        </ColumnContainerBasic>
      </SingleElementContainer>
    </>
  );
};

export default AboutUs;
