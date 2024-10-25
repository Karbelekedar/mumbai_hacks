import ArrowRight from "@/app/assets/arrow-right.svg";
import Logo from "@/app/assets/logosaas.png";
import MenuIcon from "@/app/assets/menu.svg";
import Image from "next/image";

export const Header = () => {
  return (
    <header className="sticky top-0 backdrop-blur-sm z-20">

      <div className="py-5">
        <div className="container">
          <div className="flex items-center justify-between">
            {/* Use Image for regular images */}
            <Image src={Logo} alt="Saas Logo" height={40} width={40} />
            {/* Use MenuIcon as a component directly */}
            <MenuIcon className="h-5 w-5 md:hidden" />

            <nav className="hidden md:flex gap-6 text-black/60 items-center">
              <button className="bg-black text-white px-4 py-2 rounded-lg font-medium inline-flex align-items justify-center tracking-tight">Sign In</button>
            </nav>
          </div>
        </div>
      </div>
    </header>
  );
};