"use client";

import React, { useEffect, useState } from "react";
import { HoverBorderGradient } from "@/components/ui/hover-border-gradient";
import { AuroraBackground } from "@/components/ui/aurora-background";
import { ModeToggle } from "@/components/ui/mode-toggle";
import { BackgroundGradient } from "@/components/ui/background-gradient";
import Image from "next/image";
import { Badge } from "@/components/ui/badge"
import { FaThumbsUp, FaRegThumbsUp, FaThumbsDown, FaRegThumbsDown } from "react-icons/fa6";
import { cn } from "@/lib/utils";
import Link from "next/link";

export default function Home() {
  const baseQuotesUrl = 'http://0.0.0.0:8000/quotes/';

  function getPreviousVote(guid: string) {
    const interaction = localStorage.getItem(guid);

    if (interaction !== null) {
      return interaction;
    }

    return null;
  }

  const [quoteData, setQuoteData] = useState(null); // State to hold quote data
  const [loading, setLoading] = useState(true); // Loading state

  const likeQuote = async () => {
    let response;
    let queryParams;
    const previousVote = getPreviousVote(guid);


    if (!previousVote) {
      localStorage.setItem(guid, 'like');
      queryParams = new URLSearchParams({ direction: 'increase' })
      response = await fetch(baseQuotesUrl + guid + "/like/?" + queryParams.toString(), { method: "PATCH" });
    } else {
      if (previousVote === 'like') {
        localStorage.removeItem(guid);
        queryParams = new URLSearchParams({ direction: 'decrease' })
        response = await fetch(baseQuotesUrl + guid + "/like/?" + queryParams.toString(), { method: "PATCH" });
      } else {
        localStorage.setItem(guid, 'like');
        queryParams = new URLSearchParams({ direction: 'increase', reverse_opposite: 'true' })
        response = await fetch(baseQuotesUrl + guid + "/like/?" + queryParams.toString(), { method: "PATCH" });
      }
    }

    const data = await response.json();
    const imageResponse = await Promise.resolve(
      fetch(data.image_url, { method: 'head' }).catch(() => null)
    );

    data.is_image_accessible = imageResponse?.ok || false;
    setQuoteData(data); // Save the data to state
  }

  const dislikeQuote = async () => {
    let response;
    let queryParams;
    const previousVote = getPreviousVote(guid);

    if (!previousVote) {
      localStorage.setItem(guid, 'dislike');
      queryParams = new URLSearchParams({ direction: 'increase' })
      response = await fetch("http://0.0.0.0:8000/quotes/" + guid + "/dislike/?" + queryParams.toString(), { method: "PATCH" });
    } else {
      if (previousVote === 'dislike') {
        localStorage.removeItem(guid);
        queryParams = new URLSearchParams({ direction: 'decrease' })
        response = await fetch("http://0.0.0.0:8000/quotes/" + guid + "/dislike/?" + queryParams.toString(), { method: "PATCH" });
      } else {
        localStorage.setItem(guid, 'dislike');
        queryParams = new URLSearchParams({ direction: 'increase', reverse_opposite: 'true' })
        response = await fetch("http://0.0.0.0:8000/quotes/" + guid + "/dislike/?" + queryParams.toString(), { method: "PATCH" });
      }
    }

    const data = await response.json();
    const imageResponse = await Promise.resolve(
      fetch(data.image_url, { method: 'head' }).catch(() => null)
    );

    data.is_image_accessible = imageResponse?.ok || false;
    setQuoteData(data); // Save the data to state
  }

  useEffect(() => {
    // Fetching data from the Quote API
    const fetchQuotes = async () => {
      try {
        // TODO: continue with this functionality
        const response = await fetch("http://0.0.0.0:8000/quotes/get_random_quote/");
        const data = await response.json();
        const imageResponse = await Promise.resolve(
          fetch(data.image_url, { method: 'head' }).catch(() => null)
        );

        data.is_image_accessible = imageResponse?.ok || false;
        setQuoteData(data); // Save the data to state
      } catch (error) {
        console.error("Error fetching quote data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuotes();
  }, []);

  if (loading) return <p>Loading...</p>;

  if (!quoteData) return <p>No quote data.</p>;

  const {
    guid,
    author,
    quote_text,
    category,
    likes,
    dislikes,
    image_url,
    image_alt_text,
    is_image_accessible
  } = quoteData;

  return (
    <AuroraBackground>
      <div className="absolute top-10 right-10 z-50">
        <ModeToggle />
      </div>
      <div>
        <BackgroundGradient className="rounded-lg p-3 sm:p-10 bg-white dark:bg-zinc-900">
          <div
            className={cn(
              "overflow-hidden relative card min-h-80 w-[500px] rounded-lg backgroundImage p-4",
              { "shadow-xl": is_image_accessible }
            )}
            style={is_image_accessible ? {
              backgroundImage: `url(${image_url})`,
              backgroundSize: "cover",
              backgroundPosition: "center"
            } : {}}
          >
            {is_image_accessible && (
              <div className="backdrop-blur-sm absolute inset-0 bg-black bg-opacity-50 pointer-events-none"></div>
            )}
            <div className="flex flex-col justify-center">
              <p className={cn(
                "text-base sm:text-xl mt-4 mb-2 font-bold z-10",
                {
                  "text-neutral-50 dark:text-neutral-50": is_image_accessible,
                  "text-neutral-600 dark:text-neutral-50": !is_image_accessible,
                }
              )}>
                &quot;{quote_text}&quot;
              </p>
              <p className={cn(
                "text-sm italic z-10",
                {
                  "text-neutral-300 dark:text-neutral-300": is_image_accessible,
                  "text-neutral-400 dark:text-neutral-500": !is_image_accessible,
                }
              )}>
                {author['name']}
              </p>
            </div>
          </div>

          <div className="flex justify-between mt-12">
            <button onClick={likeQuote}
                    className={cn(
                      "px-6 py-2 bg-transparent border-2 dark:text-white text-black rounded-lg font-bold " +
                      "transform hover:-translate-y-1 transition duration-400",
                      { "border-green-700 dark:border-green-700": getPreviousVote(guid) === 'like' },
                      { "border-black dark:border-white": getPreviousVote(guid) !== 'like' },
                    )}>

              {getPreviousVote(guid) === 'like' ? <FaThumbsUp className="text-green-700" /> : <FaRegThumbsUp />}
              <span>{likes}</span>
            </button>
            <div className="align-middle content-center">
              <Badge>{category['name']}</Badge>
            </div>
            <button onClick={dislikeQuote}
                    className={cn(
                      "px-6 py-2 bg-transparent border-2 dark:text-white text-black rounded-lg font-bold " +
                      "transform hover:-translate-y-1 transition duration-400",
                      { "border-red-700 dark:border-red-700": getPreviousVote(guid) === 'dislike' },
                      { "border-black dark:border-white": getPreviousVote(guid) !== 'dislike' },
                    )}>
              {getPreviousVote(guid) === 'dislike' ? <FaThumbsDown className="text-red-700" /> : <FaRegThumbsDown />}
              <span>{dislikes}</span>
            </button>
            {/*<HoverBorderGradient*/}
            {/*  containerClassName="rounded-full"*/}
            {/*  as="button"*/}
            {/*  className="dark:bg-black bg-white text-black dark:text-white flex items-center space-x-1"*/}
            {/*>*/}
            {/*  <FaRegThumbsUp onClick={likeQuote} />*/}
            {/*  <span>{likes}</span>*/}
            {/*</HoverBorderGradient>*/}
            {/*<HoverBorderGradient*/}
            {/*  containerClassName="rounded-full"*/}
            {/*  as="button"*/}
            {/*  className="dark:bg-black bg-white text-black dark:text-white flex items-center space-x-1"*/}
            {/*>*/}
            {/*  <FaRegThumbsDown onClick={dislikeQuote} />*/}
            {/*  <span>{dislikes}</span>*/}
            {/*</HoverBorderGradient>*/}
          </div>
        </BackgroundGradient>
      </div>
      {/*<CardContainer className="inter-var">*/}
      {/*  /!*<BackgroundGradient className="rounded-xl bg-white dark:bg-zinc-900">*!/*/}
      {/*  <CardBody*/}
      {/*    className="bg-gray-50 relative group/card  dark:hover:shadow-2xl dark:hover:shadow-emerald-500/[0.1] dark:bg-black dark:border-white/[0.2] border-black/[0.1] w-auto sm:w-[30rem] h-auto rounded-xl p-6 border">*/}
      {/*    <CardItem translateZ="50" className="w-full">*/}
      {/*      <div className="w-full group/card">*/}
      {/*        <div*/}
      {/*          className={cn(*/}
      {/*            " cursor-pointer overflow-hidden relative card h-96 rounded-xl shadow-xl backgroundImage flex flex-col justify-between p-4"*/}
      {/*          )}*/}
      {/*          style={is_image_accessible ? {*/}
      {/*            backgroundImage: `url(${image_url})`,*/}
      {/*            backgroundSize: "cover",*/}
      {/*            backgroundPosition: "center"*/}
      {/*          } : {}}*/}
      {/*        >*/}
      {/*          <div*/}
      {/*            className="absolute w-full h-full top-0 left-0 transition duration-300  opacity-60"></div>*/}
      {/*          <div className="absolute top-0 left-0 w-full h-full bg-black opacity-50"></div>*/}
      {/*          <CardItem translateZ={100}>*/}
      {/*            <div className="flex flex-col justify-center">*/}
      {/*              <CardItem translateZ={90}>*/}
      {/*              <h2 className="font-bold text-xl md:text-2xl text-gray-50 relative z-10">*/}
      {/*                &quot;{quote_text}&quot;*/}
      {/*              </h2>*/}
      {/*                </CardItem>*/}
      {/*              <p className="font-normal text-sm text-gray-50 relative z-10 my-4">*/}
      {/*                {author['name']}*/}
      {/*              </p>*/}
      {/*            </div>*/}
      {/*          </CardItem>*/}
      {/*        </div>*/}
      {/*      </div>*/}
      {/*    </CardItem>*/}
      {/*    <div className="flex justify-between items-center mt-20">*/}
      {/*      <CardItem*/}
      {/*        translateZ={50}*/}
      {/*        as="button"*/}
      {/*        // as={Link}*/}
      {/*        // href="https://twitter.com/mannupaaji"*/}
      {/*        // target="__blank"*/}
      {/*        // className="px-4 py-2 rounded-xl text-xs font-normal dark:text-white"*/}
      {/*        className="px-4 py-2 rounded-xl bg-black dark:bg-white dark:text-black text-white text-xs font-bold"*/}
      {/*        onClick={likeQuote}*/}
      {/*      >*/}

      {/*        <FaRegThumbsUp onClick={likeQuote} /> {likes}*/}
      {/*      </CardItem>*/}
      {/*      <CardItem*/}
      {/*        translateZ={50}*/}
      {/*      >*/}
      {/*        /!*<div className="m-40 flex justify-center text-center">*!/*/}
      {/*        <HoverBorderGradient*/}
      {/*          containerClassName="rounded-full"*/}
      {/*          as="button"*/}
      {/*          className="dark:bg-black bg-white text-black dark:text-white flex items-center space-x-2"*/}
      {/*        >*/}
      {/*          <span>Aceternity UI</span>*/}
      {/*        </HoverBorderGradient>*/}
      {/*        /!*</div>*!/*/}
      {/*      </CardItem>*/}
      {/*      <CardItem*/}
      {/*        translateZ={50}*/}
      {/*      >*/}
      {/*        <Badge>{category['name']}</Badge>*/}
      {/*      </CardItem>*/}
      {/*      <CardItem*/}
      {/*        translateZ={50}*/}
      {/*        as="button"*/}
      {/*        className="px-4 py-2 rounded-xl bg-black dark:bg-white dark:text-black text-white text-xs font-bold"*/}
      {/*        onClick={dislikeQuote}*/}
      {/*      >*/}
      {/*        <FaRegThumbsDown /> {dislikes}*/}
      {/*      </CardItem>*/}
      {/*    </div>*/}
      {/*  </CardBody>*/}
      {/*  /!*</BackgroundGradient>*!/*/}
      {/*</CardContainer>*/}
    </AuroraBackground>
  );
}
