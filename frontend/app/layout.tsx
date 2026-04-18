import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Cartographer AI — Plan your perfect journey",
  description: "Six specialized AI agents craft your complete travel itinerary — destination, budget, bookings, and local secrets.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
