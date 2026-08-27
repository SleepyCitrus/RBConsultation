import PageLayout from "@/src/components/layout/page-layout";
import { Card, loadCards } from "@/src/lib/card-loader";
import Image from "next/image";

export default async function RevealsPage() {
  const cards = await loadCards("ven", 1);

  return (
    <PageLayout title="Reveals">
      <div className="justify-left flex flex-wrap gap-4 p-4">
        {cards.map((card: Card) => (
          <div className="flex basis-45 items-center justify-center overflow-hidden" key={card.id}>
            <Image
              src={card.media.image_url}
              alt={card.name}
              width={0}
              height={0}
              sizes="100vw"
              style={{ width: "100%", height: "auto" }}
              loading="eager"
              priority
              className={`${card.orientation === "landscape" ? "scale-[1.3965] rotate-90" : ""}`}
            />
          </div>
        ))}
      </div>
    </PageLayout>
  );
}
