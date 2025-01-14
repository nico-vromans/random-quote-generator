"use client";

import Link from "next/link";
import React, { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge"

import { CardBody, CardContainer, CardItem } from "@/components/ui/3d-card";

import { BackgroundGradient } from "@/components/ui/background-gradient";

import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import { AuroraBackground } from "@/components/ui/aurora-background";
import { ModeToggle } from "@/components/ui/mode-toggle";

export default function Home() {
  const [quoteData, setQuoteData] = useState(null); // State to hold quote data
  const [loading, setLoading] = useState(true); // Loading state

  useEffect(() => {
    // Fetching data from the Quote API
    const fetchQuotes = async () => {
      try {
        // TODO: continue with this functionality
        const response = await fetch("http://0.0.0.0:8000/quotes/get_random_quote/");
        const data = await response.json();
        console.log('data', data);
        setQuoteData(data); // Save the data to state
      } catch (error) {
        console.error("Error fetching quote data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuotes();
  }, []);

  // if (loading) return <p>Loading...</p>;
  //
  // if (!quoteData) return <p>No quote data.</p>;

  // const { quote, author, category, image, likeCount, dislikeCount } = quoteData;

  return (
    <AuroraBackground>
      <div className="z-50">
        <ModeToggle />
      </div>
      <motion.div
        initial={{ opacity: 0.0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{
          delay: 0.3,
          duration: 0.8,
          ease: "easeInOut",
        }}
        className="relative flex flex-col gap-4 items-center justify-center px-4"
      >

        <CardContainer className="inter-var">
          <BackgroundGradient className="rounded-xl bg-white dark:bg-zinc-900">
            <CardBody
              className="bg-gray-50 relative group/card  dark:hover:shadow-2xl dark:hover:shadow-emerald-500/[0.1] dark:bg-black dark:border-white/[0.2] border-black/[0.1] w-auto sm:w-[30rem] h-auto rounded-xl p-6 border  ">
              <CardItem translateZ="50" className="w-full">
                <div className="w-full group/card">
                  <div
                    className={cn(
                      " cursor-pointer overflow-hidden relative card h-96 rounded-xl shadow-xl backgroundImage flex flex-col justify-between p-4",
                      "bg-[url(https://images.unsplash.com/photo-1544077960-604201fe74bc?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1651&q=80)] bg-cover"
                    )}
                  >
                    <div
                      className="absolute w-full h-full top-0 left-0 transition duration-300 group-hover/card:bg-black opacity-60"></div>
                    <CardItem>
                      <div className="flex flex-col justify-center">
                        <h2 className="font-bold text-xl md:text-2xl text-gray-50 relative z-10">
                          &quot;Some life inspiring quote.&quot;
                        </h2>
                        <p className="font-normal text-sm text-gray-50 relative z-10 my-4">
                          The Author
                        </p>
                      </div>
                    </CardItem>
                  </div>
                </div>
                {/*<Image*/}
                {/*  src="https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2560&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"*/}
                {/*  height="1000"*/}
                {/*  width="1000"*/}
                {/*  className="h-60 w-full object-cover rounded-xl group-hover/card:shadow-xl"*/}
                {/*  alt="thumbnail"*/}
                {/*/>*/}
              </CardItem>
              <div className="flex justify-between items-center mt-20">
                <CardItem
                  translateZ={20}
                  as={Link}
                  href="https://twitter.com/mannupaaji"
                  target="__blank"
                  className="px-4 py-2 rounded-xl text-xs font-normal dark:text-white"
                >
                  LIKE
                </CardItem>
                <CardItem
                  translateZ={20}
                >
                  <Badge>Category</Badge>
                </CardItem>
                <CardItem
                  translateZ={20}
                  as="button"
                  className="px-4 py-2 rounded-xl bg-black dark:bg-white dark:text-black text-white text-xs font-bold"
                >
                  DISLIKE
                </CardItem>
              </div>
            </CardBody>
          </BackgroundGradient>
        </CardContainer>

      </motion.div>
    </AuroraBackground>
    //   <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
    //     <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
    //       <Image
    //         className="dark:invert"
    //         src="/next.svg"
    //         alt="Next.js logo"
    //         width={180}
    //         height={38}
    //         priority
    //       />
    //       <ol className="list-inside list-decimal text-sm text-center sm:text-left font-[family-name:var(--font-geist-mono)]">
    //         <li className="mb-2">
    //           Get started by editing{" "}
    //           <code className="bg-black/[.05] dark:bg-white/[.06] px-1 py-0.5 rounded font-semibold">
    //             src/app/page.tsx
    //           </code>
    //           .
    //         </li>
    //         <li>Save and see your changes instantly.</li>
    //       </ol>
    //
    //       <div className="flex gap-4 items-center flex-col sm:flex-row">
    //         <a
    //           className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
    //           href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
    //           target="_blank"
    //           rel="noopener noreferrer"
    //         >
    //           <Image
    //             className="dark:invert"
    //             src="/vercel.svg"
    //             alt="Vercel logomark"
    //             width={20}
    //             height={20}
    //           />
    //           Deploy now
    //         </a>
    //         <a
    //           className="rounded-full border border-solid border-black/[.08] dark:border-white/[.145] transition-colors flex items-center justify-center hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:min-w-44"
    //           href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
    //           target="_blank"
    //           rel="noopener noreferrer"
    //         >
    //           Read our docs
    //         </a>
    //       </div>
    //     </main>
    //     <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
    //       <a
    //         className="flex items-center gap-2 hover:underline hover:underline-offset-4"
    //         href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
    //         target="_blank"
    //         rel="noopener noreferrer"
    //       >
    //         <Image
    //           aria-hidden
    //           src="/file.svg"
    //           alt="File icon"
    //           width={16}
    //           height={16}
    //         />
    //         Learn
    //       </a>
    //       <a
    //         className="flex items-center gap-2 hover:underline hover:underline-offset-4"
    //         href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
    //         target="_blank"
    //         rel="noopener noreferrer"
    //       >
    //         <Image
    //           aria-hidden
    //           src="/window.svg"
    //           alt="Window icon"
    //           width={16}
    //           height={16}
    //         />
    //         Examples
    //       </a>
    //       <a
    //         className="flex items-center gap-2 hover:underline hover:underline-offset-4"
    //         href="https://nextjs.org?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
    //         target="_blank"
    //         rel="noopener noreferrer"
    //       >
    //         <Image
    //           aria-hidden
    //           src="/globe.svg"
    //           alt="Globe icon"
    //           width={16}
    //           height={16}
    //         />
    //         Go to nextjs.org →
    //       </a>
    //     </footer>
    //   </div>
  );
}
