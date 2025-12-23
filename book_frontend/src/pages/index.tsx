import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

// Module data
const modules = [
  {
    id: 1,
    title: 'Module 1: The Robotic Nervous System',
    description: 'Explore ROS 2 concepts including nodes, topics, services, and actions that form the nervous system of robotic applications.',
    path: '/docs/modules/ros2/chapter-1-physical-ai'
  },
  {
    id: 2,
    title: 'Module 2: The Digital Twin',
    description: 'Create and work with physics-based simulations using Gazebo and high-fidelity rendering with Unity for safe robot development.',
    path: '/docs/modules/digital-twin/chapter-1-introduction'
  },
  {
    id: 3,
    title: 'Module 3: The AI-Robot Brain',
    description: 'Implement computer vision, SLAM, navigation, and perception systems using NVIDIA Isaac frameworks.',
    path: '/docs/modules/isaac/chapter-1-ai-brain'
  },
  {
    id: 4,
    title: 'Module 4: The Vision-Language-Action Pipeline',
    description: 'Build vision-language-action pipelines that enable robots to understand natural language commands and execute complex tasks.',
    path: '/docs/modules/vla/chapter-1-overview'
  }
];

function ModuleCard({ title, description, path }: { title: string; description: string; path: string }) {
  return (
    <Link to={path} className={styles.moduleCard}>
      <Heading as="h3">{title}</Heading>
      <p>{description}</p>
    </Link>
  );
}


function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx(styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className={clsx(styles.title)}>
          {siteConfig.title}
        </Heading>
        <p className={styles.subtitle}>
          A comprehensive guide to humanoid robotics, covering the complete technology stack required to develop, simulate, and deploy intelligent robotic systems.
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/preface">
            Read the Book - Start Here
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="A comprehensive guide to humanoid robotics">
      <div className={styles.mainPage}>
        <HomepageHeader />

        <section className={styles.modulesContainer}>
          <div className="container">
            <Heading as="h2" className={styles.title}>
              Core Modules
            </Heading>
            <p className={styles.subtitle}>
              Explore the four foundational pillars of humanoid robotics
            </p>
            <div className={styles.modulesGrid}>
              {modules.map((module) => (
                <ModuleCard
                  key={module.id}
                  title={module.title}
                  description={module.description}
                  path={module.path}
                />
              ))}
            </div>
          </div>
        </section>

      </div>
    </Layout>
  );
}
